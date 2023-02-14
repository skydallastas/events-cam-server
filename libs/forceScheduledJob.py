import requests

base_url = "https://24ed073a-eb48-414a-80b2-cbd67368fdd2.mock.pstmn.io/"
session = requests.Session()


def call_function(json_body):
    job_id = ""
    service_key = json_body["serviceKey"]
    status = json_body["status"]
    startDate = json_body["startDate"]
    stopDate = json_body["stopDate"]

    token = call_login()
    if not token:
        return "errore nel login"
    channel_uid = get_channel_uid(token, service_key)
    if channel_uid:
        job_id = force_job(token, channel_uid, status, startDate, stopDate)

    return {"JobId": job_id}


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


def force_job(token, channel_uid, status, startDate, stopDate):
    try:
        url = base_url + "ems/forceJobScheduled"
        response = session.post(url, json={"channelUUID": channel_uid,
                                           "status": status, "startDate": startDate, "stopDate": stopDate})
        response_json = response.json()

        print(response_json)
        return response_json["jobUUID"]
    except Exception as exc:
        print("Error {}".format(exc))
        return None
