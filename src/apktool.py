import os

from flask import current_app as app

from src.utility import construct_command, clean


def apktool(filename):
    input_path = os.path.join(app.config['APK_FOLDER_PATH'], filename)
    output_path = os.path.join(app.config['SOURCE_CODE_FOLDER_PATH'], 'apktool', filename)
    clean(output_path)

    command = construct_command(app.config['APKTOOL_COMMAND'], input_path, output_path)
    os.system(command)
    return output_path
