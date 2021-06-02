import os

from flask import current_app as app


def commit(filename):
    cmd = app.config['COMMIT'].format(filename=filename)
    os.system(cmd)
