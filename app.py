import os

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


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
    app.run()
