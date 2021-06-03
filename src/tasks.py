from celery import shared_task

from flask import current_app as app
from src.decompiler import decompile
from src.git import commit
from src.sourcegraph import update_host


def process(filename):
    decompilers = app.config['DECOMPILERS']
    for decompiler in decompilers:
        process_each(filename, decompiler)
    commit(filename)
    update_host()


@shared_task(name='tasks.process')
def process_each(filename, decompiler):
    decompile(filename, decompiler)
