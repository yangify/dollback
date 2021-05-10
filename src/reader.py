def read_file(path):
    try:
        return read_text_file(path)
    except UnicodeDecodeError:
        return read_binary_file(path)


def read_text_file(path):
    f = open(path, 'r')
    try:
        return f.readlines()
    finally:
        f.close()


def read_binary_file(path):
    f = open(path, 'rb', buffering=0)
    try:
        return f.readlines()
    finally:
        f.close()
