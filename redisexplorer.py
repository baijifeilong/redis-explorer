import json
import re

from PySide2 import QtGui, QtWidgets, QtCore
from redis.client import StrictRedis


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Redis Explorer")
        self.resize(QtWidgets.QDesktopWidget().availableGeometry(self).size() * 0.5)
        self.tree = QtWidgets.QTreeWidget()
        self.label = QtWidgets.QTextEdit()
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)
        self.tree.setColumnCount(2)
        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.setHeaderHidden(True)
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self.tree)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)
        splitter.addWidget(scroll_area)
        splitter.setSizes([1, 1])
        self.setCentralWidget(splitter)
        toolbar = self.addToolBar("")
        toolbar.setMovable(False)
        toolbar.setIconSize(QtCore.QSize(32, 32))
        toolbar.addAction(QtGui.QIcon("resources/list-add.png"), "").triggered.connect(lambda: self.plus_font(1))
        toolbar.addAction(QtGui.QIcon("resources/list-remove.png"), "").triggered.connect(lambda: self.plus_font(-1))
        toolbar.addAction(QtGui.QIcon("resources/view-refresh.png"), "").triggered.connect(lambda: self.refresh())
        self.redis = StrictRedis()

        def item_clicked(item: QtWidgets.QTreeWidgetItem):
            if item.parent() is None:
                return
            value = self.redis.get(item.text(0))
            value = value.decode()
            text = json.dumps(json.loads(value), ensure_ascii=False, indent=4)
            text = text.replace("  ", "&nbsp;").replace("\n", "<br/>").replace(":", "<font color=red>:</font>")
            text = re.sub(r'"(.*?)(?<!\\)"', r'<font color=green>"\g<1>"</font>', text)
            self.label.setHtml(text)

        self.tree.itemClicked.connect(item_clicked)

    def plus_font(self, number: int):
        font = self.label.font()
        font.setPointSize(font.pointSize() + number)
        self.label.setFont(font)

    def refresh(self):
        self.tree.clear()
        self.label.setPlainText("")
        keys = sorted(self.redis.keys("*"))
        keys = [x.decode() for x in keys]
        dct = dict()
        for key in keys:
            parts = key.split(":")
            prefix = parts[0]
            if prefix not in dct:
                dct[prefix] = [key]
            else:
                dct[prefix].append(key)
        for prefix, keys in dct.items():
            item = QtWidgets.QTreeWidgetItem([prefix])
            for key in keys:
                item.addChild(QtWidgets.QTreeWidgetItem([key]))
            self.tree.addTopLevelItem(item)

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)
        self.refresh()


def main():
    QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.show()
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    return QtWidgets.QApplication.exec_()


if __name__ == '__main__':
    main()
