import re

from src import reader


def scrape(paths):
    output = {}
    for i, path in enumerate(paths):
        # print("Scraping... {}/{}".format(i+1, len(paths)), end='\r')
        link_found = scrape_one(path)
        if len(link_found) > 0:
            output[path] = link_found
    return output


def scrape_one(path):
    output = []
    file_content = reader.read_file(path)
    for line in file_content:
        expression = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
        deep_expression = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
        basic_expression = r"(?P<url>https?://[^\s]+)"
        try:
            found = re.findall(basic_expression, line)
            found = filter_noise(found)
        except TypeError:
            continue
        output += found
    return output


def filter_noise(url_list):
    output = [url for url in url_list if is_noise(url)]
    return output


def is_noise(url):
    block_list = get_block_list()
    for block_url in block_list:
        if block_url in url:
            return False
    return True


def get_block_list():
    return [
        "schemas.android.com",
        "google.com",
        "facebook.com",
        "w3.org",
        "jquery.org",
        "apache.org",
        "requirejs.org",
        "JSON.org",
        "example.com",
        "googleads.g.doubleclick.net",
        "googlemobileadssdk.page.link",
        "pagead2.googlesyndication.com",
    ]
