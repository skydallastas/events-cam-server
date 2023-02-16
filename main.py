from flask import Flask, request
from libs import forceJob, updateDb, forceScheduledJob, jobDetails

app = Flask(__name__)


@app.get('/jobs/<jobUUID>')
def job_details(jobUUID):
    try:
        return jobDetails.call_function(jobUUID)
    except Exception as exc:
        print("Error {}".format(exc))


@app.post('/updateDb')
def update_db():
    try:
        print("Request {}".format(request.endpoint))
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_body = request.json
        else:
            return 'Content-Type not supported!'

        print("body {}".format(json_body))
        return updateDb.call_function(json_body)
    except Exception as exc:
        print("Error {}".format(exc))

@app.post('/forceJob')
def force_job():
    try:
        print("Request {}".format(request.endpoint))
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_body = request.json
        else:
            return 'Content-Type not supported!'

        print("body {}".format(json_body))

        return forceJob.call_function(json_body)
    except Exception as exc:
        print("Error {}".format(exc))




@app.post('/forceScheduledJob')
def force_job_scheduled():
    try:
        print("Request {}".format(request.endpoint))
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_body = request.json
        else:
            return 'Content-Type not supported!'

        print("body {}".format(json_body))

        return forceScheduledJob.call_function(json_body)
    except Exception as exc:
        print("Error {}".format(exc))


if __name__ == '__main__':
    try:
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        print(e)
