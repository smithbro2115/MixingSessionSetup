from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from .DesignerFiles import loginDialog
import qdarkstyle


class DialogTemplate(QtWidgets.QDialog):
    def __init__(self, ui, parent=None):
        super(DialogTemplate, self).__init__(parent=parent)
        self.ui = ui()
        self.ui.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class LoginDialogSigs(QtCore.QObject):
    accepted = pyqtSignal(tuple)
    canceled = pyqtSignal()


class LoginDialog(QtWidgets.QDialog):
    def __init__(self, website, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.signals = LoginDialogSigs()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.ui = loginDialog.Ui_login()
        self.ui.setupUi(self)
        self.ui.loginSiteName.setText(f'Login into {website}')


class GetFileLocationDialog(QtWidgets.QFileDialog):
    def __init__(self, default_name, caption, default_location=None):
        super(GetFileLocationDialog, self).__init__()
        self.caption = caption
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.default_location = default_location if default_location else '/'
        self.default_name = default_name

    def get_save_path(self):
        result = self.getSaveFileName(directory=f'{self.default_location}{self.default_name}', caption=self.caption)[0]
        return result

    def get_file_path(self, file_types):
        result = self.getOpenFileName(self, self.caption, self.default_location, file_types)
        return result


class GetFolderLocationDialog(QtWidgets.QFileDialog):
    def __init__(self, caption, default_location=None):
        super(GetFolderLocationDialog, self).__init__()
        self.caption = caption
        self.default_location = default_location if default_location else '/'

    def get_save_path(self):
        result = self.getExistingDirectory(directory=f'{self.default_location}', caption=self.caption)
        return result


def add_scripts_to_list_widget(scripts, list_widget: QtWidgets.QListWidget):
    list_widget.clear()
    for script in scripts:
        item = QtWidgets.QListWidgetItem(script['title'])
        item.setData(8, script)
        list_widget.addItem(item)


def show_error(window, error):
    msg_box = QtWidgets.QMessageBox()
    msg_box.about(window, "ERROR", str(error))
