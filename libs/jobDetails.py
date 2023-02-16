import requests
import boto3

base_url_login = "https://01e32dc1-123c-4978-8572-545b2b79ed65.mock.pstmn.io/"
session = requests.Session()

EXPIRED = 90
FAILED = 80
NO_ACTION_LOCKED = 21
NO_ACTION_REQUIRED = 20
DONE = 10
IN_PROGRESS = 5
PENDING_RETRY = 3
PLANNED = 0
TOKEN_EXPIRED = 401


def call_function(jobUUID):
    try:
        token = getTokenOnDB()
        if not token:
            saveTokenOnDB(call_login())

        status = 0
        response_json = ""
        url = getBaseUrlOnDB() + "ems/jobs"
        # Viene chiamato EMS fino a quando non si riceve una risposta di OK / KO
        while True:
            response = requests.get(url, params=jobUUID)
            response_json = response.json()
            status = response_json["status"]
            if status == TOKEN_EXPIRED:
                saveTokenOnDB(call_login())
                continue
            if status != PENDING_RETRY or status != IN_PROGRESS:
                break
        return response_json
    except Exception as exc:
        print("Error {}".format(exc))
        return None

def getTokenOnDB():
    try:
        client = boto3.client('dynamodb')
        response = client.get_item(
            TableName='config',
            Key={
                "id": {
                    "S": 'ems_api'
                }
            }
        )
        return response['Item']['token']['S']
    except Exception as exc:
        print("Error {}".format(exc))

def getBaseUrlOnDB():
    try:
        client = boto3.client('dynamodb')
        response = client.get_item(
            TableName='config',
            Key={
                "id": {
                    "S": 'ems_api'
                }
            }
        )
        print(response)
        return response['Item']['base_url']['S']
    except Exception as exc:
        print("Error {}".format(exc))

def saveTokenOnDB(newToken):
    try:
        client = boto3.client('dynamodb')
        data = client.put_item(
            TableName='config',
            Item={
                "id": {
                    "S": 'ems_api'
                },
                "token": {
                    "S": newToken
                },
                "username": {
                    "S": 'user1'
                },
                "password": {
                    "S": 'psw1'
                },
                "base_url": {
                    "S": getBaseUrlOnDB()
                }
            }
        )
    except Exception as exc:
        print("Error {}".format(exc))


def call_login():
    try:
        url = base_url_login + "ems/login"
        request_body = {"username": "admin", "password": "admin"}
        response = session.post(url, json=request_body)
        response_json = response.json()
        return response_json["token"]
    except Exception as exc:
        print("Error {}".format(exc))
        return None