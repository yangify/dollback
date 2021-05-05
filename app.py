import os

from flask import Flask, render_template, request
from flask_celery import make_celery

from time import sleep

app = Flask(__name__)
app.config.from_pyfile('config.py')

celery = make_celery(app)


@app.route('/')
def hello_world():
    for i in range(5):
        test.delay()
    return 'Hello World!'


@app.route('/queue')
def inspect_queue():
    i = celery.control.inspect()
    current_active = i.active()
    scheduled = i.scheduled()
    reserved = i.reserved()

    return {
        'active': current_active,
        'scheduled': scheduled,
        'reserved': reserved
        }


@celery.task(name='app.test')
def test():
    sleep(30)
    return 'success'


@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Files required'

    if not os.path.exists("./resources/apk"):
        os.makedirs("./resources/apk")

    file = request.files['file']
    file.save('./resources/apk/' + file.filename)
    return 'Success'


if __name__ == '__main__':
    app.run(debug=True)
