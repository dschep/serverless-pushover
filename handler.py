import json
import os
import re
from datetime import datetime

from botocore.vendored import requests


def webhook(event, context):
    print(event["body"])
    payload = json.loads(event["body"])

    params = {
        "token": os.environ.get("PUSHOVER_APP_KEY"),
        "user": os.environ.get("PUSHOVER_USER_KEY"),
        "device": os.environ.get("DEVICE"),
        "priority": os.environ.get("PRIORITY", 0),
        "sound": os.environ.get("SOUND", "pushover"),
    }
    if payload.get("ping"):
        params["message"] = event["body"]
        params["title"] = "Test Notification"
        params["monospace"] = 1
    elif payload.get("insight"):
        params["timestamp"] = datetime.strptime(
            payload["timestamp"], "%Y-%m-%dT%H:%M:%SZ"
        ).timestamp()
        params["html"] = 1
        params["url_title"] = "View Insight"
        params["url"] = payload["url"]
        params[
            "message"
        ] = f"""{payload["description"]}

<b>detected at</b>
&nbsp;&nbsp;&nbsp;&nbsp;{payload["timestamp"]}
<b>function</b>
&nbsp;&nbsp;&nbsp;&nbsp;{payload["target"]["function"]}
<b>service</b>
&nbsp;&nbsp;&nbsp;&nbsp;{payload["target"]["service"]}
<b>application</b>
&nbsp;&nbsp;&nbsp;&nbsp;{payload["target"]["application"]}
<b>org</b>
&nbsp;&nbsp;&nbsp;&nbsp;{payload["target"]["tenant"]}"""
        # TODO - more detail per notification type:
        # if payload.get("insight") == "EscalatedInvocationCount":
        #     message += f"""  more info """
        params["title"] = re.sub(r'([a-z])([A-Z])', r'\1 \2', payload["insight"])
    else:
        params["monospace"] = 1
        params["message"] = (json.dumps(payload, indent=2),)
        params["title"] = "Unknown notification payload"

    resp = requests.post("https://api.pushover.net/1/messages.json", json=params)

    resp.raise_for_status()

    return {"statusCode": 200}
