import logging

from flask import Flask
from flask_cors import CORS

from blueprint.apk import apk
from blueprint.configuration import configuration
from blueprint.detection import detection
from blueprint.link import link
from database.db import mongo

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(apk)
app.register_blueprint(detection)
app.register_blueprint(configuration)
app.register_blueprint(link)
CORS(app)
mongo.init_app(app)


@app.route('/')
def home():
    return 'Welcome to dollback'


if __name__ == '__main__':
    app.run(debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
