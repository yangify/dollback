import os
import platform

from flask import current_app as app

from src.utility import construct_command


def jadx(filename):
    input_path = os.path.join(app.config['APK_FOLDER_PATH'], filename)
    output_path = os.path.join(app.config['SOURCE_CODE_FOLDER_PATH'], 'jadx', filename)

    command = construct_command(app.config['JADX_COMMAND'], input_path, output_path)
    if platform.system().lower() == 'linux':
        command = "sh " + command
    os.system(command)
    return output_path
