import os
import sys
import configparser
from PyQt5.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject
import traceback


def try_to_add_section_to_config(ini_file, section):
    try:
        ini_file.add_section(section)
    except configparser.DuplicateSectionError:
        pass


def write_to_ini_file(category, option, value, path):
    cache = configparser.ConfigParser()
    try_to_add_section_to_config(cache, category)
    cache.read(path)
    cache.set(category, str(option), str(value))
    with open(path, 'w') as cache_file:
        cache.write(cache_file)


def read_from_ini_file(category, option, path):
    cache = configparser.ConfigParser()
    cache.read(path)
    return cache.get(category, option)


def write_to_cache(category, option, value):
    cache_path = f"{get_app_data_folder('')}/cache.ini"
    write_to_ini_file(category, option, value, cache_path)


def read_from_cache(category, option):
    cache_path = f"{get_app_data_folder('')}/cache.ini"
    return read_from_ini_file(category, option, cache_path)


def make_folder_if_it_does_not_exist(src, folder):
    new_src = src.replace('\\', '/')
    directory = f"{new_src}/{folder}"
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    return directory


def get_app_data_folder(folder):
    app_data_path = os.getenv('APPDATA')
    app_path = make_folder_if_it_does_not_exist(app_data_path, 'MixingSessionSetup')
    return make_folder_if_it_does_not_exist(app_path, folder)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.interrupt = False

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            if not self.interrupt:
                self.signals.finished.emit()  # Done

