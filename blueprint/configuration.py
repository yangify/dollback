from bson import ObjectId
from flask import Blueprint, request

from database.db import mongo

configuration = Blueprint('configuration', __name__)


@configuration.route('/api/configuration', methods=['GET', 'POST', 'PUT'])
@configuration.route('/api/configuration/<_id>', methods=['DELETE'])
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
