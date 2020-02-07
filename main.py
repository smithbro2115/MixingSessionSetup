from PyQt5 import QtWidgets
from GUI.DesignerFiles import MainWindowUI
import qdarkstyle


class UI(MainWindowUI.Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.main_window = None

    def setup_additional(self, main_window):
        self.main_window = main_window
        self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, gui_ui):
        super(MainWindow, self).__init__()
        self.ui = gui_ui

    def closeEvent(self, *args, **kwargs):
        super(MainWindow, self).close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    mainWindow = MainWindow(ui)
    ui.setupUi(mainWindow)
    ui.setup_additional(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
