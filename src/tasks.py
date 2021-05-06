from time import sleep

from app import celery


@celery.task(name='app.test')
def test():
    sleep(30)
    return 'success'
