import requests

base_url = "https://46af8fe3-e595-4caf-9ea4-7e4cc174fa3c.mock.pstmn.io/"
STATUS_OK = 20
STATUS_KO = 10

def call_function(jobUUID):
    try:
        status = 0
        response_json = ""
        url = base_url + "ems/jobs"
        # Viene chiamato EMS fino a quando non si riceve una risposta di OK / KO
        while True:
            response = requests.get(url, params=jobUUID)
            response_json = response.json()
            status = response_json["status"]
            if status == STATUS_OK or status == STATUS_KO:
                break
        return response_json
    except Exception as exc:
        print("Error {}".format(exc))
        return None
