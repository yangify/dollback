import os

from flask import Flask, request
from flask_cors import CORS, cross_origin

from src.flask_celery import make_celery
from src.tasks import process
from src.utility import save

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

celery = make_celery(app)


@app.route('/api/upload', methods=['POST'])
@cross_origin()
def upload():
    i = request
    file = request.files['file']
    file_path = save(file)
    # process.delay(file, file_path)
    return "Success"




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


@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Files required'

    if not os.path.exists("./resources/apk"):
        os.makedirs("./resources/apk")

    file = request.files['file']
    file.save('./resources/apk/' + file.filename)
    return 'Success'


if __name__ == '__main__':
    app.run(debug=True)
