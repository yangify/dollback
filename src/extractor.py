import os

from flask import current_app as app
from flask_pymongo import PyMongo

from src import crawler, scraper


def extract_and_save(filename, decompiler):
    findings = extract(filename, decompiler)
    save(findings, filename, decompiler)


def extract(filename, decompiler):
    source_path = os.path.join(app.config['SOURCE_CODE_FOLDER_PATH'], decompiler, filename)
    files = crawler.get_files(source_path)
    return scraper.scrape(files)


def save(findings, filename, decompiler):
    mongo = PyMongo(app)
    document = {
        "name": filename,
        "decompiler": decompiler,
        "detections": findings
    }
    if mongo.db.apks.find_one({"name": filename, "decompiler": decompiler}) is None:
        mongo.db.apks.insert_one(document)
    else:
        mongo.db.apks.find_one_and_update({"name": filename, "decompiler": decompiler}, {"$set": document})
