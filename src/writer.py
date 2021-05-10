import json
import os

from flask import current_app as app


def write(content, filename, decompiler):
    create_output_directory(decompiler)
    output_path = os.path.join(app.config['LINK_FOLDER_PATH'], decompiler, filename + ".json")
    json_output = json.dumps(content, indent=4)

    f = open(output_path, "w")
    f.write(json_output)
    f.close()
    return output_path


def create_output_directory(tool):
    if not os.path.exists(app.config['LINK_FOLDER_PATH']):
        os.mkdir(app.config['LINK_FOLDER_PATH'])

    path = os.path.join(app.config['LINK_FOLDER_PATH'], tool)
    if not os.path.exists(path):
        os.mkdir(path)
