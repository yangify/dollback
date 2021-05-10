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
    if not os.path.exists("./resources/output"):
        os.mkdir("./resources/output")

    if not os.path.exists("./resources/output/" + tool):
        os.mkdir("./resources/output/" + tool)
