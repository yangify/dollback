from flask import Blueprint, request

from src.sourcegraph import search
from database.db import mongo

detection = Blueprint('detection', __name__)


@detection.route('/api/link')
def get_links():
    filename = request.args.get('filename')
    if filename == '' or filename is None:
        return {'data': []}

    response = {'filename': filename, 'results': []}
    groups = list(mongo.db.configuration.find({}))
    for group in groups:
        result = {
            'groupName': group['groupName'],
            'data': []
        }
        for query in group['data']:
            query_output = {
                'title': query['title'],
                'query': query['search_term'],
                'data': search(query, filename)
            }
            result['data'].append(query_output)
        response['results'].append(result)

    db_action(filename, response)
    return response


def db_action(filename, response):
    if mongo.db.link.find_one({'filename': filename}) is not None:
        mongo.db.link.delete_one({'filename': filename})
    mongo.db.link.insert(response)

    data = mongo.db.link.find_one_or_404({'filename': filename})
    response['_id'] = str(data['_id'])
