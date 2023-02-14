import requests

base_url = "https://46af8fe3-e595-4caf-9ea4-7e4cc174fa3c.mock.pstmn.io/"

def call_function(token):
    try:
        # Viene chiamato EMS fino a quando non si riceve una risposta di OK / KO
        listRresponseEMS = ["a", "b", "OK", "KO"]
        responseEMS = call_EMS(listRresponseEMS)
        url = base_url + "ems/jobdetails"
        response = requests.get(url, params=responseEMS)
        response_json = response.json()
        print(response_json)
        return response_json
    except Exception as exc:
        print("Error {}".format(exc))
        return None

def call_EMS(listRresponseEMS):
    for resp in listRresponseEMS:
        if (resp.__eq__('OK') or resp.__eq__('KO')):
            return resp
            break
