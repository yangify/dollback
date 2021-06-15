import json

from bson import ObjectId
from flask import Blueprint, request

from database.db import mongo

configuration = Blueprint('configuration', __name__)


@configuration.route('/api/configuration',          methods=['GET', 'POST'])
@configuration.route('/api/configuration/<_id>',    methods=['PUT', 'DELETE'])
def configure(_id=None):

    if request.method == 'GET':
        data = list(mongo.db.configuration.find({}))
        for d in data:
            d['_id'] = str(d['_id'])
        return {'data': data}

    if request.method == 'POST':
        data = json.loads(request.data)
        mongo.db.configuration.insert_one(data)
        return 'post success'

    if request.method == 'PUT':
        return 'put success'

    if request.method == 'DELETE':
        data = mongo.db.configuration.find_one({'_id': ObjectId(_id)})
        if data is not None:
            data['_id'] = str(data['_id'])

        output = mongo.db.configuration.delete_one({'_id': ObjectId(_id)})
        return {'data': dict(data)} if output.deleted_count == 1 else {'data': {}}

    return 'nothing processed'
