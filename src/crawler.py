from os import listdir
from os.path import isfile, join
from collections.abc import Iterable


def get_files(path):
    items = listdir(path)
    fat_list = get_file_list(path, items)
    return [file for file in flatten(fat_list)]


def get_file_list(path, items):
    return [join(path, item) if isfile(join(path, item)) else get_files(join(path, item)) for item in items]


def flatten(fat_list):
    for el in fat_list:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el
