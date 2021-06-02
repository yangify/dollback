from flask import current_app as app

from app import mongo


@app.route('/insertone')
def insert_one():
    output = mongo.db.apks.insert_one({"test": "test"})
    return str(output)


@app.route('/findall')
def find_all():
    cursor = mongo.db.apks.find({})
    output = list(cursor)
    return str(output)


@app.route('/findone')
def find_one():
    output = mongo.db.apks.find_one({'name': 'updated'})
    return str(output)


@app.route('/updateone')
def update_one():
    # update will add missing fields
    output = mongo.db.apks.find_one_and_update({'name': 'refreshed'}, {'$set': {'type': 'something'}})
    return str(output)


@app.route('/replaceone')
def replace_one():
    # replace will just wipe all old and insert new
    output = mongo.db.apks.find_one_and_replace({'name': 'refreshed'}, {'new': 'new'})
    return str(output)

