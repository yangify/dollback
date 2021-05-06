import os

from flask import current_app as app


def save(file):

    if not os.path.exists(app.config['APK_FOLDER_PATH']):
        os.makedirs(app.config['APK_FOLDER_PATH'])

    filename = file.filename.replace(' ', '_')
    file.save(app.config['APK_FOLDER_PATH'] + filename)
