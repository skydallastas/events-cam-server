import requests

base_url = "https://5bef51e4-5b5a-47c0-bc0e-16b81a6f53b2.mock.pstmn.io/"

def call_function(json_body):
    try:
        jobId = json_body["serviceKey"]
        url = base_url + "updateDb"
        # aggiungere logica che chiama appSync ed aggiorna il dynamo
        response = requests.post(url, json=json_body)
        response_json = response.json()
        print(response_json)
        return response_json["response"]
    except Exception as exc:
        print("Error {}".format(exc))
        return


