import json
import os


def write(content, filename, tool):
    json_output = json.dumps(content, indent=4)
    create_output_directory(tool)

    output_path = os.path.join("./resources/output", tool, filename + ".json")

    f = open(output_path, "w")
    f.write(json_output)
    f.close()
    return output_path


def create_output_directory(tool):
    if not os.path.exists("./resources/output"):
        os.mkdir("./resources/output")

    if not os.path.exists("./resources/output/" + tool):
        os.mkdir("./resources/output/" + tool)
