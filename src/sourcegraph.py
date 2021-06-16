import requests

from flask import current_app as app


def search(query, repo_name):
    json_query = craft_query(query, repo_name)
    data, status_code = send_request(json_query)
    return craft_results(data)


def craft_query(meta_query, repo_name):
    search_term = meta_query['search_term']
    pattern_type = meta_query['pattern_type']
    search_query = app.config['SOURCEGRAPH_SEARCH_QUERY'] \
        .replace('<REPO_NAME>', repo_name) \
        .replace('<SEARCH_TERM>', search_term) \
        .replace('<PATTERN_TYPE>', pattern_type)
    return {
        "query": search_query,
        "variables": None
    }


def craft_results(data):
    response = []
    for result in data['data']['search']['results']['results']:
        filename = result['file']['name']
        filepath = result['file']['path']
        for line_match in result['lineMatches']:
            start = line_match['offsetAndLengths'][0][0]
            end = line_match['offsetAndLengths'][0][1]
            line = line_match['preview']

            result = craft_result(filename, filepath, line, start, end)
            response.append(result)

    return response


def craft_result(filename, filepath, line, start, end):
    return {
        'file':
            {
                'name': filename,
                'path': filepath
            },
        'link': line[start: start + end]
    }


def send_request(json_query):
    url = app.config['SOURCEGRAPH_URL'] + app.config['SOURCEGRAPH_API']
    headers = {'Authorization': 'token ' + app.config['SOURCEGRAPH_TOKEN']}
    r = requests.post(url, headers=headers, json=json_query)
    return r.json(), r.status_code


def update_host():
    host_id = app.config['SOURCEGRAPH_LOCALHOST']
    url = app.config['SOURCEGRAPH_URL'] + app.config['SOURCEGRAPH_API']
    headers = {'Authorization': 'token ' + app.config['SOURCEGRAPH_TOKEN']}
    json = {'query': app.config['SOURCEGRAPH_UPDATE_HOST_QUERY'].replace('{host_id}', host_id),
            'variables': None,
            'operationName': 'UpdateExternalService'}

    r = requests.post(url, headers=headers, json=json)
    return r.status_code
