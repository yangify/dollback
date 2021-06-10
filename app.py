import logging
import gridfs

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from src.flask_celery import make_celery
from src.tasks import process
from src.utility import save
from src.sourcegraph import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

celery = make_celery(app)
mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.cx.dollback)


@app.route('/')
def home():
    return 'Welcome to dollback'


@app.route('/api/upload', methods=['POST'])
@cross_origin()
def upload():
    file = request.files['file']
    filename, filepath = save(file)
    if not fs.exists(filename=filename):
        mongo.save_file(filename, file)
    process(filename)
    return "Success"


@app.route('/api/download/<filename>')
def download(filename):
    return mongo.send_file(filename)


@app.route('/api/apk', methods=['GET'])
@app.route('/api/apk/<_id>', methods=['DELETE'])
def get_apk(_id=None):
    if request.method == 'GET':
        return {'apks': [{'_id': str(grid_out._id), 'name': grid_out.name, 'date': str(grid_out.upload_date)} for grid_out in fs.find()]}

    if request.method == 'DELETE':
        fs.delete(ObjectId(_id))
        return {'id': _id}


@app.route('/api/link')
def get_link():
    filename = request.args.get('filename')

    data = get_links(filename)
    data['filename'] = filename

    if mongo.db.link.find_one({'filename': filename}) is not None:
        mongo.db.link.delete_one({'filename': filename})
    mongo.db.link.insert(data)

    data = mongo.db.link.find_one_or_404({'filename': filename})
    data['_id'] = str(data['_id'])
    return data


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


@app.route('/api/configuration', methods=['GET', 'POST', 'PUT'])
@app.route('/api/configuration/<_id>', methods=['DELETE'])
def configure(_id=None):

    if request.method == 'GET':
        data = list(mongo.db.configuration.find({}))
        for d in data:
            d['_id'] = str(d['_id'])
        return {'data': data}

    if request.method == 'POST':
        title = request.form['title']
        query = request.form['query']
        data = {'title': title, 'query': query}
        mongo.db.configuration.insert_one(data)

    if request.method == 'PUT':
        return 'put success'

    if request.method == 'DELETE':
        data = mongo.db.configuration.find_one({'_id': ObjectId(_id)})
        if data is not None:
            data['_id'] = str(data['_id'])

        output = mongo.db.configuration.delete_one({'_id': ObjectId(_id)})
        return {'data': dict(data)} if output.deleted_count == 1 else {'data': {}}

    return 'nothing processed'


if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)