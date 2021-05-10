import os
import time

from flask import Flask, request
from flask_cors import CORS, cross_origin

from src.flask_celery import make_celery
from src.tasks import process
from src.utility import save

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

celery = make_celery(app)


@app.route('/api/upload', methods=['POST'])
@cross_origin()
def upload():
    file = request.files['file']
    filename, filepath = save(file)
    process(filename)
    return "Success"


@app.route('/api/apk')
def apk_list():
    response = []
    apks = os.listdir(app.config['APK_FOLDER_PATH']) if os.path.exists(app.config['APK_FOLDER_PATH']) else []
    for apk in apks:
        response.append({
            'name': apk,
            'date': time.ctime(os.path.getctime(app.config['APK_FOLDER_PATH'] + '/' + apk))
        })
    return {'apks': response}


@app.route('/api/queue')
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


if __name__ == '__main__':
    app.run(debug=True)
