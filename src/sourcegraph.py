import requests

from flask import current_app as app


def query(json_query):
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


def get_links(repo_name):
    json_query = {
        "query": app.config['SOURCEGRAPH_SEARCH_URL'].replace('<REPO_NAME>', repo_name),
        "variables": None
    }
    data, status_code = query(json_query)

    output = []
    for result in data['data']['search']['results']['results']:
        filename = result['file']['name']
        filepath = result['file']['path']
        for line_match in result['lineMatches']:
            start = line_match['offsetAndLengths'][0][0]
            end = line_match['offsetAndLengths'][0][1]
            line = line_match['preview']

            output_object = {
                'file': {
                    'name': filename,
                    'path': filepath
                },
                'link': line[start: start+end]
            }
            output.append(output_object)
    return {'data': output}
