import subprocess

from flask import current_app as app


def commit_and_push(filename):
    # TODO
    print(filename)


def create_repository(repository_name):
    cmd = app.config['CREATE_REPOSITORY_CMD'].format(repository_name=repository_name).split()
    output = subprocess.run(cmd)
    return output.returncode == 0


def clone(repository_name):
    username = app.config['CODECOMMIT_USERNAME']
    password = app.config['CODECOMMIT_PASSWORD']
    cmd = app.config['CLONE_REPOSITORY_CMD'].format(username=username, password=password, repository_name=repository_name).split()
    output = subprocess.run(cmd)
    return output.returncode == 0
