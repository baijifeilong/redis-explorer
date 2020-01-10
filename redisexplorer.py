import json

from PySide2 import QtGui, QtWidgets
from redis.client import StrictRedis


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Redis Explorer")
        self.resize(QtWidgets.QDesktopWidget().availableGeometry(self).size() * 0.5)
        self.tree = QtWidgets.QTreeWidget()
        self.label = QtWidgets.QLabel()
        self.tree.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored))
        self.tree.setColumnCount(2)
        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.setHeaderHidden(True)
        self.label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored))
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.label)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.redis = StrictRedis()

        def item_clicked(item: QtWidgets.QTreeWidgetItem):
            if item.parent() is None:
                return
            value = self.redis.get(item.text(0))
            value = value.decode()
            text = json.dumps(json.loads(value), ensure_ascii=False, indent=4)
            self.label.setText(text)

        self.tree.itemClicked.connect(item_clicked)

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)
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


def main():
    QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.show()
    return QtWidgets.QApplication.exec_()


if __name__ == '__main__':
    main()
