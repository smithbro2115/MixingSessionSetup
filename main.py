from PyQt5 import QtWidgets, QtCore
from GUI.DesignerFiles import MainWindowUI
from Functionality import useful_utils
from configparser import NoOptionError, NoSectionError
from GUI import CustomGUI
import os
import qdarkstyle
from Celtx import CeltxScraper
from ProTools.SessionCreation import make_session
from Auth.Credentials import get_credentials, Canceled
from Spreadsheet import SpreadsheetCreation
from Functionality.Email import email_excel_document


class UI(MainWindowUI.Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.main_window = None
        self.celtx_scraper = CeltxScraper.CeltxHook(self.get_celtx_credentials)
        self.current_script = None
        self.thread_pool = QtCore.QThreadPool()
        self.current_html = None
        self.file_location_line_edits = []

    def setup_additional(self, main_window):
        self.main_window = main_window
        self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.celtxScriptsListWidget.itemDoubleClicked.connect(self.celtx_list_item_double_clicked)
        self.populateCeltxPushButton.clicked.connect(self.populate_celtx_scripts_list)
        self.makeSFXListPushButton.clicked.connect(self.make_sfx_list_pushed)
        self.set_up_line_edits()
        self.newSessionNameLineEdit.set_with_celtx = False
        self.file_location_line_edits = [self.sessionTemplateLineEdit,
                                         self.oldSessionLocationLineEdit,
                                         self.newSessionLocationLineEdit,
                                         self.emailAddressLineEdit,
                                         self.newSessionNameLineEdit]
        self.saved_field_line_edits(self.file_location_line_edits[:-1])
        self.set_up_file_location_line_edits(self.file_location_line_edits)
        self.enable_make_session_button_if_file_locations()
        self.makeSFXListPushButton.setEnabled(False)
        self.setupPushButton.clicked.connect(self.setup_clicked)
        self.makeNewSessionPushButton.clicked.connect(self.make_new_session_clicked)
        self.populate_celtx_scripts_list()
        self.validate()

    def saved_field_line_edits(self, line_edits):
        for line_edit in line_edits:
            line_edit.save_field = True
        self.emailAddressLineEdit.save_field = True

    def set_up_line_edits(self):
        self.newSessionNameLineEdit.text_validator = CustomGUI.FieldValidator()
        self.newSessionNameLineEdit.text_validator.add_rule(CustomGUI.field_not_empty)
        required_directory_validator = CustomGUI.FieldValidator()
        required_directory_validator.add_rule(CustomGUI.field_is_directory)
        self.sessionTemplateLineEdit.text_validator = required_directory_validator
        self.newSessionLocationLineEdit.text_validator = required_directory_validator
        self.oldSessionLocationLineEdit.text_validator = CustomGUI.FieldValidator()
        self.oldSessionLocationLineEdit.text_validator.add_rule(CustomGUI.field_is_file)
        self.oldSessionLocationLineEdit.text_validator.add_rule(lambda x: os.path.splitext(x.text())[1] == ".ptx")
        self.newSessionNameLineEdit.editingFinished.connect(
            lambda: self.file_location_line_edit_changed(self.newSessionNameLineEdit))
        self.sessionTemplateLineEdit.editingFinished.connect(
            lambda: self.file_location_line_edit_changed(self.sessionTemplateLineEdit))
        self.sessionTemplateLocationToolButton.clicked.connect(
            lambda: self.file_location_line_edit_button_clicked(self.sessionTemplateLineEdit))
        self.oldSessionLocationLineEdit.editingFinished.connect(
            lambda: self.file_location_line_edit_changed(self.oldSessionLocationLineEdit))
        self.oldSessionLocationToolButton.clicked.connect(self.old_session_line_edit_button_clicked)
        self.newSessionLocationLineEdit.editingFinished.connect(
            lambda: self.file_location_line_edit_changed(self.newSessionLocationLineEdit))
        self.newSessionLocationToolButton.clicked.connect(
            lambda: self.file_location_line_edit_button_clicked(self.newSessionLocationLineEdit))
        self.emailAddressLineEdit.editingFinished.connect(
            lambda: self.file_location_line_edit_changed(self.emailAddressLineEdit))

    def setup_clicked(self):
        if self.validate():
            self.make_sfx_list_pushed()
            self.make_new_session_clicked()

    def make_new_session_clicked(self):
        try:
            make_session(self.sessionTemplateLineEdit.text(),
                         self.newSessionLocationLineEdit.text(),
                         self.newSessionNameLineEdit.text())
        except FileExistsError:
            CustomGUI.show_error(self.main_window, "This session already exists!")
        os.startfile(self.oldSessionLocationLineEdit.text())

    def populate_celtx_scripts_list(self):
        try:
            scripts = self.celtx_scraper.get_celtx_scripts()
            CustomGUI.add_scripts_to_list_widget(scripts, self.celtxScriptsListWidget)
        except CeltxScraper.LoginError:
            CustomGUI.show_error(self.main_window, "Network error! You may want to try different credentials.")
        except Canceled:
            pass

    def set_up_file_location_line_edits(self, line_edits):
        for line_edit in line_edits:
            self.load_last_used_text_into_line_edit(line_edit)

    def validate(self):
        self.enable_make_session_button_if_file_locations()
        valid = self.makeNewSessionPushButton.isEnabled() and self.makeSFXListPushButton.isEnabled()
        self.setupPushButton.setEnabled(valid)
        return valid

    def validate_file_location_line_edits(self):
        for line_edit in self.file_location_line_edits:
            try:
                if not line_edit.text_validator.validate(line_edit):
                    return False
            except AttributeError:
                continue
        return True

    def enable_make_session_button_if_file_locations(self):
        self.makeNewSessionPushButton.setEnabled(self.validate_file_location_line_edits())

    def file_location_line_edit_button_clicked(self, line_edit):
        dialog = CustomGUI.GetFolderLocationDialog("Set Save Location", default_location=line_edit.text())
        path = dialog.get_save_path()
        line_edit.setText(path)
        self.file_location_line_edit_changed(line_edit)

    def old_session_line_edit_button_clicked(self):
        text = self.get_pro_tools_session_location(self.oldSessionLocationLineEdit.text())
        if text != '':
            self.oldSessionLocationLineEdit.setText(text)
        self.file_location_line_edit_changed(self.oldSessionLocationLineEdit)

    @staticmethod
    def load_last_used_text_into_line_edit(line_edit):
        try:
            if line_edit.save_field:
                last_used = useful_utils.read_from_cache("LAST_USED_LINE_EDIT_TEXT", line_edit.objectName())
                line_edit.setText(last_used)
        except (NoOptionError, NoSectionError, AttributeError):
            pass

    def file_location_line_edit_changed(self, line_edit):
        name = line_edit.objectName()
        useful_utils.write_to_cache("LAST_USED_LINE_EDIT_TEXT", name, line_edit.text())
        self.newSessionNameLineEdit.set_with_celtx = False
        self.validate()

    @staticmethod
    def get_pro_tools_session_location(location):
        dialog = CustomGUI.GetFileLocationDialog("", "Get Pro Tools Session File", default_location=location)
        path = dialog.get_file_path('*.ptx')
        return path[0]

    def make_sfx_list_pushed(self):
        try:
            dialog = CustomGUI.GetFileLocationDialog(f"{self.current_script['title']} SFX List.xlsx", "Make SFX List",
                                                     useful_utils.read_from_cache("LAST_USED", "sfx_list_folder"))
            save_path = dialog.get_save_path()
            if save_path != "":
                self.make_sfx_list(save_path)
        except (NoOptionError, NoSectionError):
            useful_utils.write_to_cache("LAST_USED", "sfx_list_folder",
                                        f"{useful_utils.get_app_data_folder('SFX Lists')}/")
            self.make_sfx_list_pushed()

    def make_sfx_list(self, save_path):
        self.write_last_used_sfx_list_path(save_path)
        SpreadsheetCreation.create_new_sfx_list_spreadsheet(save_path)
        SpreadsheetCreation.populate_spreadsheet(save_path,
                                                 CeltxScraper.get_scenes_and_sounds_from_html(self.current_html))
        try:
            email_excel_document(save_path, self.emailAddressLineEdit.text())
        except:
            pass

    @staticmethod
    def write_last_used_sfx_list_path(path):
        dir_path = os.path.dirname(path)
        useful_utils.write_to_cache("LAST_USED", "sfx_list_folder", f"{dir_path}/")

    def celtx_list_item_double_clicked(self, item):
        self.current_script = item.data(8)
        self.display_script(self.current_script)
        self.makeSFXListPushButton.setEnabled(True)
        self.validate()

    def display_script(self, script):
        self.scriptTextBrowser.clear()
        self.current_html = self.celtx_scraper.get_script_html(script)
        html = self.current_html.decode()
        self.scriptTextBrowser.setHtml(html)
        if self.newSessionNameLineEdit.text() == "" or self.newSessionNameLineEdit.set_with_celtx:
            self.newSessionNameLineEdit.setText(CeltxScraper.format_script_title(script['title']))
            self.newSessionNameLineEdit.set_with_celtx = True

    @staticmethod
    def get_celtx_credentials():
        return get_credentials("celtx")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, gui_ui):
        super(MainWindow, self).__init__()
        self.ui = gui_ui

    def closeEvent(self, *args, **kwargs):
        super(MainWindow, self).close()


if __name__ == '__main__':
    import sys

    print(os.listdir("Z:/"))
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    mainWindow = MainWindow(ui)
    ui.setupUi(mainWindow)
    ui.setup_additional(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
