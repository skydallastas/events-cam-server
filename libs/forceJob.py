import requests

base_url = "https://0fcd62e4-2f2b-435b-b541-cc66b3bc3227.mock.pstmn.io/"

def call_function(json_body):
    jobId = json_body["serviceKey"]

    login = call_login()
    if not login:
        return "errore nel login"
    channelUid = get_channel_uid()
    if channelUid:
        jobId = force_job()

    return {"JobId": jobId}


def call_login():
    try:
        url = base_url + "ems/login"
        request_body = {"username": "admin", "password": "admin"}
        response = requests.post(url, json=request_body)
        response_json = response.json()

        print(response_json)
        return response_json["isLogged"]  # TODO
    except Exception as exc:
        print("Error {}".format(exc))
        return


def get_channel_uid():
    try:
        url = base_url + "ems/getChannelUUID"  # TODO
        response = requests.get(url)
        response_json = response.json()

        print(response_json)
        return response_json["channelUid"]
    except Exception as exc:
        print("Error {}".format(exc))
        return


def force_job():
    try:
        url = base_url + "ems/forceJob" #TODO
        response = requests.post(url)
        response_json = response.json()

        print(response_json)
        return response_json["jobId"]
    except Exception as exc:
        print("Error {}".format(exc))
        return
