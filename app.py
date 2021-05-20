import json
import os
import time

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo

from src.flask_celery import make_celery
from src.tasks import process
from src.utility import save

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

celery = make_celery(app)

mongo = PyMongo(app)


@app.route('/insertone')
def insert_one():
    output = mongo.db.apks.insert_one({"test": "test"})
    return str(output)


@app.route('/findall')
def find_all():
    cursor = mongo.db.apks.find({})
    output = list(cursor)
    return str(output)


@app.route('/findone')
def find_one():
    output = mongo.db.apks.find_one({'name': 'updated'})
    return str(output)


@app.route('/updateone')
def update_one():
    # update will add missing fields
    output = mongo.db.apks.find_one_and_update({'name': 'refreshed'}, {'$set': {'type': 'something'}})
    return str(output)


@app.route('/replaceone')
def replace_one():
    # replace will just wipe all old and insert new
    output = mongo.db.apks.find_one_and_replace({'name': 'refreshed'}, {'new': 'new'})
    return str(output)


@app.route('/api/upload', methods=['POST'])
@cross_origin()
def upload():
    file = request.files['file']
    filename, filepath = save(file)
    process(filename)
    return "Success"


@app.route('/api/apk')
def get_apk():
    response = []
    apks = os.listdir(app.config['APK_FOLDER_PATH']) if os.path.exists(app.config['APK_FOLDER_PATH']) else []
    for apk in apks:
        response.append({
            'name': apk,
            'date': time.ctime(os.path.getctime(app.config['APK_FOLDER_PATH'] + '/' + apk))
        })
    return {'apks': response}


@app.route('/api/link')
def get_link():
    filename = request.args.get('filename')
    response = {}
    for decompiler in app.config['DECOMPILERS']:
        response[decompiler] = []
        path = os.path.join(app.config['LINK_FOLDER_PATH'], decompiler, filename + '.json')

        if not os.path.exists(path):
            continue

        file = open(path)
        data = json.load(file)

        for path in data:
            for link in data[path]:
                root_path = os.path.join(app.config['SOURCE_CODE_FOLDER_PATH'], decompiler, filename)
                file_path = path.replace(root_path, '')
                response[decompiler].append({
                    'path': file_path,
                    'link': link
                })

    return response


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
