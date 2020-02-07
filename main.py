from PyQt5 import QtWidgets
from GUI.DesignerFiles import MainWindowUI
from Functionality import useful_utils
from configparser import NoOptionError, NoSectionError
from GUI import CustomGUI
import os
import qdarkstyle
from Celtx import CeltxScraper
from Auth.Credentials import get_credentials, Canceled
from Spreadsheet import SpreadsheetCreation


class UI(MainWindowUI.Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.main_window = None
        self.celtx_scraper = CeltxScraper.CeltxHook(self.get_celtx_credentials)
        self.current_script = None
        self.current_html = None

    def setup_additional(self, main_window):
        self.main_window = main_window
        self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.celtxScriptsListWidget.itemDoubleClicked.connect(self.celtx_list_item_double_clicked)
        self.populateCeltxPushButton.clicked.connect(self.populate_celtx_scripts_list)
        self.makeSFXListPushButton.clicked.connect(self.make_sfx_list_pushed)
        self.makeSFXListPushButton.setEnabled(False)
        self.populate_celtx_scripts_list()

    def populate_celtx_scripts_list(self):
        try:
            scripts = self.celtx_scraper.get_celtx_scripts()
            CustomGUI.add_scripts_to_list_widget(scripts, self.celtxScriptsListWidget)
        except CeltxScraper.LoginError:
            CustomGUI.show_error(self.main_window, "Network error! You may want to try different credentials.")
        except Canceled:
            pass

    def make_sfx_list_pushed(self):
        try:
            dialog = CustomGUI.GetFileLocationDialog(f"test SFX List.xlsx", "Make SFX List",
                                                     useful_utils.read_from_cache("LAST_USED", "sfx_list_folder"))
            save_path = dialog.get_save_path()
            self.write_last_used_sfx_list_path(save_path)
            SpreadsheetCreation.create_new_sfx_list_spreadsheet(save_path)
            SpreadsheetCreation.populate_spreadsheet(save_path,
                                                     CeltxScraper.get_scenes_and_sounds_from_html(self.current_html))
        except (NoOptionError, NoSectionError):
            useful_utils.write_to_cache("LAST_USED", "sfx_list_folder",
                                        f"{useful_utils.get_app_data_folder('SFX Lists')}/")
            self.make_sfx_list_pushed()

    @staticmethod
    def write_last_used_sfx_list_path(path):
        dir_path = os.path.dirname(path)
        useful_utils.write_to_cache("LAST_USED", "sfx_list_folder", f"{dir_path}/")

    def celtx_list_item_double_clicked(self, item):
        self.current_script = item.data(8)
        self.display_script(self.current_script)
        self.makeSFXListPushButton.setEnabled(True)

    def display_script(self, script):
        self.scriptTextBrowser.clear()
        self.current_html = self.celtx_scraper.get_script_html(script)
        print(self.current_html)
        html = self.current_html.decode()
        self.scriptTextBrowser.setHtml(html)

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
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    mainWindow = MainWindow(ui)
    ui.setupUi(mainWindow)
    ui.setup_additional(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
