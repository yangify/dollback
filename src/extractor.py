import os

from flask import current_app as app

from src import crawler, writer, scraper


def extract(filename, decompiler):
    source_path = os.path.join(app.config['SOURCE_CODE_FOLDER_PATH'], decompiler, filename)
    files = crawler.get_files(source_path)
    findings = scraper.scrape(files)
    return writer.write(findings, filename, decompiler)
