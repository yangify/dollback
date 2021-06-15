import gridfs
from bson import ObjectId
from flask import Blueprint, request
from flask_cors import cross_origin

from database.db import mongo
from src.tasks import process
from src.utility import save

apk = Blueprint('apk', __name__)


@apk.route('/api/apk', methods=['GET'])
@apk.route('/api/apk/<_id>', methods=['DELETE'])
def get_apk(_id=None):
    fs = gridfs.GridFS(mongo.cx.dollback)
    if request.method == 'GET':
        return {'apks': [{'_id': str(grid_out._id), 'name': grid_out.name, 'date': str(grid_out.upload_date)} for grid_out in fs.find()]}

    if request.method == 'DELETE':
        fs.delete(ObjectId(_id))
        return {'id': _id}


@apk.route('/api/upload', methods=['POST'])
@cross_origin()
def upload():
    fs = gridfs.GridFS(mongo.cx.dollback)

    file = request.files['file']
    filename, filepath = save(file)
    if not fs.exists(filename=filename):
        mongo.save_file(filename, file)
    process(filename)
    return "Success"


@apk.route('/api/download/<filename>')
def download(filename):
    return mongo.send_file(filename)
