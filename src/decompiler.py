import os
import platform
import shutil
from os.path import join

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
        apktool(filename, filepath)
        return move_file(filename, tool)

    # if tool == 'jadx':
    #     jadx(filename, filepath)
    #     return move_file(filename, tool)


def apktool(filename, filepath):
    clean('./' + filename)
    command = app.config['APKTOOL_COMMAND'] + filepath
    os.system(command)


def jadx(filepath):
    path = join(os.getcwd() + "/src/decompiler/jadx/bin/jadx")
    command = "\"" + path + "\"" + " " + filepath
    if platform.system().lower() == 'linux':
        command = "sh " + command
    if platform.system().lower() == 'linux' and app.env == 'development':
        command = "sudo " + command
    os.system(command)


def move_file(filename, tool):
    folder_path = app.config['DECOMPILED_CODE_PATH'] + '/' + tool + '/' + filename
    clean(folder_path)
    shutil.move('./' + filename, folder_path)

    return folder_path
