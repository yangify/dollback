import os
import platform
import shutil

from flask import current_app as app

from src.utility import clean


def decompile(filename, filepath):
    output_paths = []
    for tool in app.config['DECOMPILERS']:
        filename_without_extension = filename[:-4]
        output_path = decompile_apk(filename_without_extension, filepath, tool)
        output_paths.append(output_path)
    return output_paths


def decompile_apk(filename, filepath, tool):
    if tool == 'apktool':
        return apktool(filename, filepath, tool)

    if tool == 'jadx':
        return jadx(filename, filepath)


def apktool(filename, filepath, tool):
    clean('./' + filename)
    command = app.config['APKTOOL_COMMAND'] + filepath
    os.system(command)
    return move_file(filename, tool)


def jadx(filename, input_path):
    output_path = app.config['DECOMPILED_CODE_FOLDER_PATH'] + '/jadx/' + filename

    command = app.config['JADX_COMMAND']
    command = command.replace('<OUTPUT_PATH>', output_path)
    command = command.replace('<INPUT_PATH>', input_path)

    if platform.system().lower() == 'linux':
        command = "sh " + command
    os.system(command)
    return output_path


def move_file(filename, tool):
    folder_path = app.config['DECOMPILED_CODE_FOLDER_PATH'] + '/' + tool + '/' + filename
    clean(folder_path)
    shutil.move('./' + filename, folder_path)
    return folder_path
