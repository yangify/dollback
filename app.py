import logging

from flask import Flask
from flask_cors import CORS

from blueprint.apk import apk
from blueprint.configuration import configuration
from database.db import mongo
from blueprint.detection import detection

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(apk)
app.register_blueprint(detection)
app.register_blueprint(configuration)
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
