import requests

from flask import current_app as app


def update_host():

    host_id = app.config['SOURCEGRAPH_LOCALHOST']
    url = app.config['SOURCEGRAPH_URL'] + app.config['SOURCEGRAPH_API']
    headers = {'Authorization': 'token ' + app.config['SOURCEGRAPH_TOKEN']}
    json = {'query': app.config['SOURCEGRAPH_UPDATE_HOST_QUERY'].replace('{host_id}', host_id),
            'variables': None,
            'operationName': 'UpdateExternalService'}

    r = requests.post(url, headers=headers, json=json)
    return r.status_code
