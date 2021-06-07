import gridfs

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo

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


@app.route('/api/apk')
def get_apk():
    return {'apks': [{'name': grid_out.name, 'date': str(grid_out.upload_date)} for grid_out in fs.find()]}


@app.route('/api/link')
def get_link():
    filename = request.args.get('filename')
    data = mongo.db.link.find_one({'filename': filename})
    if data is None:
        data = get_links(filename)
        data['filename'] = filename
        mongo.db.link.insert_one(data)
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


@app.route('/api/configuration', methods=['GET', 'POST', 'PUT', 'DELETE'])
def configure():
    if request.method == 'GET':
        query_id = request.form['_id']
        mongo.db.configuration.find_one({'_id': query_id})
        return 'get success'

    if request.method == 'POST':
        name = request.form['name']
        query = request.form['query']
        data = {'name': name, 'query': query}
        mongo.db.configuration.insert_one(data)
        return 'post success'

    if request.method == 'PUT':
        return 'put success'

    if request.method == 'DELETE':
        return 'delete success'

    return 'nothing processed'


if __name__ == '__main__':
    app.run(debug=True)
