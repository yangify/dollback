import os
import platform

from flask import current_app as app

from src.utility import clean, construct_command


def decompile(filename, decompiler):
    return decompile_apk(filename, decompiler)


def decompile_apk(filename, decompiler):
    if decompiler == 'apktool':
        return apktool(filename)

    if decompiler == 'jadx':
        return jadx(filename)


def apktool(filename):
    clean('./' + filename)

    input_path = os.path.join(app.config['APK_FOLDER_PATH'], filename)
    output_path = os.path.join(app.config['SOURCE_CODE_FOLDER_PATH'], 'apktool', filename)

    command = construct_command(app.config['APKTOOL_COMMAND'], input_path, output_path)
    os.system(command)
    return output_path


def jadx(filename):
    clean('./' + filename)

    input_path = os.path.join(app.config['APK_FOLDER_PATH'], filename)
    output_path = os.path.join(app.config['SOURCE_CODE_FOLDER_PATH'], 'jadx', filename)

    command = construct_command(app.config['JADX_COMMAND'], input_path, output_path)
    if platform.system().lower() == 'linux':
        command = "sh " + command
    os.system(command)
    return output_path
