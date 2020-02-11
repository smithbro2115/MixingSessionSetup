from ProTools import Files
from pywinauto.application import Application
import os


def make_session(template_path, old_path, new_location, new_name):
    path = Files.copy_from_template(template_path, new_location, new_name)


def test():
    make_session("Z:\\PRO TOOLS TEMPLATE FOR SOUND DESIGN", "", "Z:\\2020 Season 9 MIXING", "073 GIVER AND THE GIFT")
