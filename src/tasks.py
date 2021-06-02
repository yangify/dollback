from celery import shared_task

from flask import current_app as app
from src.decompiler import decompile
from src.git import commit


def process(filename):
    decompilers = app.config['DECOMPILERS']
    for decompiler in decompilers:
        process_each(filename, decompiler)
    commit(filename)


@shared_task(name='tasks.process')
def process_each(filename, decompiler):
    decompile(filename, decompiler)
