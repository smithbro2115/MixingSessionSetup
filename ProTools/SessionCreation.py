from ProTools import Files


def make_session(template_path, new_location, new_name):
    path = Files.copy_from_template(template_path, new_location, new_name)
    return path
