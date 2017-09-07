import os
import requests
import json
from flask import Flask, jsonify

app = Flask(__name__)

BASE_URL = 'https://cafe.cfapps.io'

@app.route('/', methods=['POST'])
def receive_slack_command():
    #json_data = request.get_json(force=True)
    devices = json.loads(requests.get(BASE_URL + '/status').text)

    attachments = []
    for device in devices:

        if (device["status"] == "UNAVAILABLE"):
            color = "#e0e4e5"
            msg = "_%s_ is *Unavailable*" % device["devId"]
        elif (device["status"] == "BREWING"):
            color = "#229be6"
            msg = "_%s_ is *Brewing*" % device["devId"]
        else:
            if (device["level"] < 33):
                color = "#f2242f"
            elif (device["level"] < 66):
                color = "#e6b822"
            else:
                color = "#8ae622"
            msg = "_%s_ is at *%d%%*" % (device["devId"], device["level"])

        deviceSlackFormatted = {
            "text": msg,
            "color": color,
            "mrkdwn_in": ["text", "pretext"]
        }

        attachments.append(deviceSlackFormatted)

    resp = {
        "response_type": "in_channel",
        "attachments": attachments
    }
    return jsonify(resp)

# run app
if __name__ == "__main__":
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        PORT = 5001
        DEBUG = True
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
        DEBUG = True

    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)