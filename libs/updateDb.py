import requests
import boto3
import json

url_garphql = "https://l32xzesthbbsjaxaksymmrbgvi.appsync-api.eu-west-1.amazonaws.com/graphql"
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


def call_list(service_key, start_date, end_date):
    list_cam = list_all_data()
    ems_body = {
        "version": "1.0",
        "territory": "UK",
        "serviceKey": service_key,
        "events": []
    }
    events = []

    for item in list_cam["data"]["listCams"]["items"]:
        event = {
            "eventId": item["ID"],
            "title": "example 1",
            "startDate": start_date,
            "endDate": end_date
        }
        events.append(event)
    # call to EMS
    ems_body["events"] = events

    return "OK"

def list_all_data():
    query = """
        query MyQuery {
            listCams {
                items {
                    ID
                    cam_name
                    service_key
                    start_date
                    end_date
                }
            }
        }
    """
    header = {
        "x-api-key": "da2-y3bayhucgzembh3yy4fxmhi2ia"
    }
    response = requests.post(url_garphql, headers=header, json={'query': query})
    print(response.status_code)
    list_cam = json.loads(response.text)

    return list_cam


def updateDynamoDb(id_cam, status):
    mutation = """
        mutation MyMutation {
            updateCams(input: {ID: "@ID", status: "@status"}) {
                ID
                status
            }
        }
    """

    header = {
        "x-api-key": "da2-y3bayhucgzembh3yy4fxmhi2ia"
    }

    mutation = mutation.replace("@ID", id_cam)
    mutation = mutation.replace("@status", status)

    response = requests.post(url_garphql, headers=header, json={'query': mutation})

    print(response.status_code)
    result = json.loads(response.text)

    return result
