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
    try:
        file = request.files['file']
        filename, filepath = save(file)
        mongo.save_file(filename, file)
        process(filename)
        return "Success"
    except:
        return "Fail"


@app.route('/api/download/<filename>')
def download(filename):
    return mongo.send_file(filename)


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
    response = {'data': []}
    cursor = mongo.db.apks.find({'name': filename})
    for document in cursor:
        document['_id'] = str(document['_id'])
        response['data'].append(document)
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
