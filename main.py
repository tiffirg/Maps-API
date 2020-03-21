import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from Interface import Interface_API


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 880, 490)
        self.title = "App"
        self.menubar = self.menuBar()
        self.central_widget = Interface_API()
        self.setCentralWidget(self.central_widget)
        self.initUI()

    def initUI(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exit_call)
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def exit_call(self):
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())