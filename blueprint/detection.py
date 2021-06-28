from flask import Blueprint, request

from src.sourcegraph import search
from database.db import mongo

detection = Blueprint('detection', __name__)


@detection.route('/api/link')
def get_links():
    response = {'data': []}
    filename = request.args.get('filename')
    if filename == '' or filename is None:
        return response

    response['filename'] = filename
    groups = list(mongo.db.configuration.find({}))
    for group in groups:
        result = {
            'groupName': group['groupName'],
            'data': []
        }
        for query in group['data']:
            query_output = {
                'title': query['title'],
                'query': query['searchTerm'],
                'data': search(query, filename)
            }
            result['data'].append(query_output)
        response['data'].append(result)

    return save(filename, response)


def save(filename, response):
    if mongo.db.link.find_one({'filename': filename}) is not None:
        mongo.db.link.delete_one({'filename': filename})
    mongo.db.link.insert(response)

    data = mongo.db.link.find_one_or_404({'filename': filename})
    data['_id'] = str(data['_id'])
    return data
