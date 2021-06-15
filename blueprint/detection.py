from flask import Blueprint, request

from src.sourcegraph import get_links
from database.db import mongo

detection = Blueprint('detection', __name__)


@detection.route('/api/link')
def get_link():
    filename = request.args.get('filename')
    if filename == '' or filename is None:
        return {'data': []}

    data = get_links(filename)
    data['filename'] = filename

    if mongo.db.link.find_one({'filename': filename}) is not None:
        mongo.db.link.delete_one({'filename': filename})
    mongo.db.link.insert(data)

    data = mongo.db.link.find_one_or_404({'filename': filename})
    data['_id'] = str(data['_id'])
    return data
