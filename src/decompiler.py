from src.apktool import apktool
from src.jadx import jadx


def decompile(filename, decompiler):
    return decompile_apk(filename, decompiler)


def decompile_apk(filename, decompiler):
    if decompiler == 'apktool':
        return apktool(filename)

    if decompiler == 'jadx':
        return jadx(filename)
