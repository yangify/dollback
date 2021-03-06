import os
import shutil

from flask import current_app as app


def save(file):
    if not os.path.exists(app.config['APK_FOLDER_PATH']):
        os.makedirs(app.config['APK_FOLDER_PATH'])

    filename = file.filename.replace(' ', '_')
    filepath = os.path.join(app.config['APK_FOLDER_PATH'], filename)
    file.save(filepath)
    return filename, filepath


def clean(filepath):
    if os.path.exists(filepath):
        shutil.rmtree(filepath)


def construct_command(command, input, output):
    command = command.replace('<INPUT_PATH>', input)
    command = command.replace('<OUTPUT_PATH>', output)
    return command
