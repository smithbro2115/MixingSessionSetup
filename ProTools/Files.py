import os
import shutil


def make_new_session(template_path, new_location, new_name):
    copy_from_template(template_path, new_location, new_name)


def copy_from_template(template_path, new_location, new_name):
    new_path = f"{new_location}/{new_name}"
    shutil.copytree(template_path, new_path)
    os.rename(get_pro_tools_file_path(new_path), f"{new_path}/{new_name}.ptx")
    return f"{new_path}/{new_name}.ptx"


def get_pro_tools_file_path(session_folder):
    for file_path in os.listdir(session_folder):
        if os.path.splitext(file_path)[1] == '.ptx':
            return f"{session_folder}/{file_path}"
