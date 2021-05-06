from celery import shared_task

from src.decompiler import decompile
from src.extractor import extract


@shared_task(name='tasks.process')
def process(filename, file_path):
    decompile(filename, file_path)
    extract(filename)
