import requests
import argparse

def _login(session: requests.Session, base_url, email, password):
    print("Login to Faraday")

    url = f"{base_url}/_api/login"
    credentials = {"email": email, "password": password}

    response = session.post(url, json=credentials)
    response.raise_for_status()

    return response

def exists_workspaces(faraday_session, base_url, workspace):
    print(f"Checking if workspace {workspace} exists")

    response = faraday_session.get(f"{base_url}/_api/v2/ws/")
    cluster = response.json()

    return [ws for ws in cluster if ws.get('name', None) == workspace] != []

def create_workspace(faraday_session, base_url, email, workspace):
    print(f"Workspace {workspace} doesn't exists. Creating it")

    url = f"{base_url}/_api/v2/ws/"
    body = {"_id": workspace, "name": workspace, "type": "Workspace", "users": [email]}

    response = faraday_session.post(url, json=body)
    response.raise_for_status()

    return response.json()

def upload_report(faraday_session, base_url, workspace, file_name):
    print(f"Uploading report in workspace {workspace}.")

    csrf_url = f"{base_url}/_api/session"
    url = f"{base_url}/_api/v2/ws/{workspace}/upload_report"
    files = {"file": open(file_name, 'r')}

    csrf_token = faraday_session.get(csrf_url).json().get('csrf_token')

    body = {"csrf_token": csrf_token}

    response = faraday_session.post(url, data=body, files=files)
    response.raise_for_status()

    return response.json()

def import_scan(base_url, email, password, workspace, file_name):
    print(f'Importing scan from {file_name}')

    faraday_session = requests.Session()
    _login(faraday_session, base_url, email, password)
    ws_exists = exists_workspaces(faraday_session, base_url, workspace)

    if not ws_exists:
        create_workspace(faraday_session, base_url, email, workspace)

    upload_report(faraday_session, base_url, workspace, file_name)
    print('Report uploaded successfully')


parser = argparse.ArgumentParser()
parser.add_argument('-b', '--base_url', metavar='base_url', type=str, help='Base url for FaradayServer server (example: http://10.20.30.40:8080)')
parser.add_argument('-e', '--email', metavar='email', type=str, help="Faraday email")
parser.add_argument('-p', '--password', metavar='password', type=str, help="Faraday password")
parser.add_argument('-f', '--file_name', metavar='file_name', type=str, help='File name for XML report')
parser.add_argument('-w', '--workspace', metavar='workspace', type=str, help='Workspace where the report will be uploaded')
args = parser.parse_args()

if __name__ == "__main__":
    import_scan(args.base_url, args.email, args.password, args.workspace, args.file_name)