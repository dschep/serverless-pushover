import json
import os
import re
from datetime import datetime

from botocore.vendored import requests


def webhook(event, context):
    print(event["body"])
    return handle_notification(json.loads(event["body"]), context)


def sns(event, context):
    for record in event["Records"]:
        handle_notification(json.loads(record["Sns"]["Message"]), context)


def handle_notification(event, context):
    params = {
        "token": os.environ.get("PUSHOVER_APP_KEY"),
        "user": os.environ.get("PUSHOVER_USER_KEY"),
        "device": os.environ.get("DEVICE"),
        "priority": os.environ.get("PRIORITY", 0),
        "sound": os.environ.get("SOUND", "pushover"),
    }
    if event.get("ping"):
        params["message"] = json.dumps(event)
        params["title"] = "Test Notification"
        params["monospace"] = 1
    elif event.get("insight"):
        params["timestamp"] = int(
            datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        )
        params["html"] = 1
        params["url_title"] = "View Insight"
        params["url"] = event["url"]
        params[
            "message"
        ] = f"""{event["description"]}

<b>detected at</b>
&nbsp;&nbsp;&nbsp;&nbsp;{event["timestamp"]}
<b>function</b>
&nbsp;&nbsp;&nbsp;&nbsp;{event["target"]["function"]}
<b>service</b>
&nbsp;&nbsp;&nbsp;&nbsp;{event["target"]["service"]}
<b>application</b>
&nbsp;&nbsp;&nbsp;&nbsp;{event["target"]["application"]}
<b>org</b>
&nbsp;&nbsp;&nbsp;&nbsp;{event["target"]["tenant"]}"""
        # TODO - more detail per notification type:
        # if event.get("insight") == "EscalatedInvocationCount":
        #     message += f"""  more info """
        params["title"] = re.sub(r"([a-z])([A-Z])", r"\1 \2", event["insight"])
    else:
        params["monospace"] = 1
        params["message"] = json.dumps(event, indent=2)
        params["title"] = "Unknown notification event"

    resp = requests.post("https://api.pushover.net/1/messages.json", json=params)

    resp.raise_for_status()

    return {"statusCode": 200}
