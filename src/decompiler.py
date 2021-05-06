import os
import platform
import shutil
from os.path import join

from flask import current_app as app


def decompile(file, file_path):
    output_paths = []
    for tool in app.config['DECOMPILERS']:
        output_path = decompile_apk(file, file_path, tool)
        output_paths.append(output_path)
    return output_paths


def decompile_apk(file, file_path, tool):
    if tool == 'apktool':
        apktool(file, file_path)

    if tool == 'jadx':
        jadx(file_path)


def apktool(file, file_path):
    command = "java -jar ./src/decompiler/apktool/apktool.jar d " + file_path
    if platform.system().lower() == 'linux' and app.env == 'development':
        command = "sudo " + command
    os.system(command)


def jadx(file_path):
    path = join(os.getcwd() + "/src/decompiler/jadx/bin/jadx")
    command = "\"" + path + "\"" + " " + file_path
    if platform.system().lower() == 'linux':
        command = "sh " + command
    if platform.system().lower() == 'linux' and app.env == 'development':
        command = "sudo " + command
    os.system(command)


def move_file(file_path, tool):
    create_output_directory(tool)
    file_name = get_file_name(file_path)

    output_path = "./resources/output/archive/" + tool
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    folder_path = "./resources/output/archive/" + tool + "/" + file_name
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    shutil.move("./" + file_name, "./resources/output/archive/" + tool)

    return output_path + "/" + file_name


def create_output_directory(tool):
    if not os.path.exists("./resources/output/archive/" + tool):
        os.makedirs("./resources/output/archive/" + tool)


def get_file_name(file_path):
    index = file_path.rfind('/')
    if index == -1:
        return remove_extension(file_path)

    file_name = file_path[index+1:]
    return remove_extension(file_name)


def remove_extension(file_name):
    return file_name[:-4]
