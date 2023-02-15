import requests
from libs import jobDetails

base_url = "https://01e32dc1-123c-4978-8572-545b2b79ed65.mock.pstmn.io/"
session = requests.Session()


def call_function(json_body):
    job_id = ""
    service_key = json_body["serviceKey"]
    status = json_body["status"]
    eventList = json_body["eventList"]
    for event in eventList:
        print('chiamo EMS')
    token = call_login()
    if not token:
        return "errore nel login"
    channel_uid = get_channel_uid(token, service_key)
    if channel_uid:
        job_id = force_job(token, channel_uid, status)
    # chiamo API jobDetails
    return jobDetails.call_function(token)
    #return {"jobUUID": job_id}


def call_login():
    try:
        url = base_url + "ems/login"
        request_body = {"username": "admin", "password": "admin"}
        response = session.post(url, json=request_body)
        response_json = response.json()

        print(response_json)
        return response_json["token"]
    except Exception as exc:
        print("Error {}".format(exc))
        return None


def get_channel_uid(token, service_key):
    try:
        url = base_url + "ems/getChannelUUID"
        params = {"serviceKey": service_key, "territory": "default"}
        response = session.get(url, params=params)
        response_json = response.json()

        print(response_json)
        return response_json["channelUUID"]
    except Exception as exc:
        print("Error {}".format(exc))
        return None


def force_job(token, channel_uid, status):
    try:
        url = base_url + "ems/forceJob"
        response = session.post(url, json={"channelUUID": channel_uid, "status": status})
        response_json = response.json()

        print(response_json)
        return response_json["jobUUID"]
    except Exception as exc:
        print("Error {}".format(exc))
        return None
