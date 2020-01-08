#include <QApplication>
#include <QWidget>

int main(int argc, char **argv) {
    new QApplication(argc, argv);
    auto window = new QWidget();
    window->setWindowTitle("Hello World");
    window->show();
    return QApplication::exec();
}
