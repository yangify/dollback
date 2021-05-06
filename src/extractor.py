from src.decompiler import decompile


def extract(file):
    decompile(file)
    return True
