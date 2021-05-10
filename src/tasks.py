from celery import shared_task

from flask import current_app as app
from src.decompiler import decompile
from src.extractor import extract


def process(filename):
    decompilers = app.config['DECOMPILERS']
    for decompiler in decompilers:
        process_each.delay(filename, decompiler)


@shared_task(name='tasks.process')
def process_each(filename, decompiler):
    decompile(filename, decompiler)
    extract(filename, decompiler)
