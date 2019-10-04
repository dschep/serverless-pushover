import json
import os
import re
import sys
from importlib import import_module


def get_user_handler(user_handler_value):
    if "/" in user_handler_value:
        user_module_path, user_module_and_handler = user_handler_value.rsplit("/", 1)
        sys.path.append(user_module_path)
    else:
        user_module_and_handler = user_handler_value

    user_module_name, user_handler_name = user_module_and_handler.split(".")
    user_module = import_module(user_module_name)
    if "/" in user_handler_value:
        sys.path.pop()

    return getattr(user_module, user_handler_name)


user_handler = get_user_handler(os.environ['USER_HANDLER'])


def sns(event, context):
    for record in event["Records"]:
        user_handler(json.loads(record["Sns"]["Message"]))
