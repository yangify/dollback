from celery import shared_task
from time import sleep


@shared_task(name='test')
def test():
    sleep(30)
    return 'success'
