import json

from flask import Blueprint

link = Blueprint('link', __name__)


@link.route('/api/android')
def get_android_link():
    f = open('resources/links/android.json', 'r')
    return {'android': json.load(f)}
