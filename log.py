import datetime
import utils

def add_log_entry(show, logfile, entry):
    if show: print(entry)

    f = open(logfile, 'a')
    f.write(str(entry))
    f.close()


class LogEntry:
    def __init__(self):
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "LogEntry: " + str(self.timestamp) + '\n'


class InitEntry(LogEntry):
    def __init__(self, last_comment):
        LogEntry.__init__(self)
        self.last_comment = last_comment

    def __repr__(self):
        return "INITENTRY: " + str(self.timestamp) + '\n' \
            + "  last_comment: " + str(self.last_comment) + '\n'


class CheckForCommands(LogEntry):
    def __init__(self, fresh_comments):
        LogEntry.__init__(self)
        self.fresh_comments = fresh_comments

    def __repr__(self):
        return "CHECKFORCOMMANDS: " + str(self.timestamp) + '\n' \
            + "  fresh_comments: " + str(self.fresh_comments) + '\n'


class CommandAndResponse(LogEntry):
    def __init__(self, cmd, data, r, out):
        LogEntry.__init__(self)
        self.cmd = cmd
        self.data = data
        self.r = r

        if cmd == utils.Command.SEND_FILE:
            # don't log files
            self.out = "<file>"
        else:
            self.out = out

    def __repr__(self):
        return "COMMANDANDRESPONSE: " + str(self.timestamp) + '\n' \
            + "  cmd: " + self.cmd.name + '\n' \
            + "  data: \"" + self.data + '\"\n' \
            + "  r: " + str(self.r) + '\n' \
            + "  out: \"" + self.out + '\"\n'


class AliveBots(LogEntry):
    def __init__(self, bots):
        LogEntry.__init__(self)
        self.bots = bots

    def __repr__(self):
        repr = "ALIVEBOTS: " + str(self.timestamp) + '\n' \
            + "  bots: " + str(len(self.bots)) + '\n'
        for id in self.bots:
            repr += "    " + str(id) + '\n'
        return repr


class Command(LogEntry):
    def __init__(self, bot, cmd, data, r):
        LogEntry.__init__(self)
        self.bot = bot
        self.cmd = cmd
        self.data = data
        self.r = r

    def __repr__(self):
        return "COMMAND: " + str(self.timestamp) + '\n' \
            + "  bot: " + str(self.bot) + '\n' \
            + "  cmd: " + self.cmd.name + '\n' \
            + "  data: \"" + self.data + '\"\n' \
            + "  r: " + str(self.r) + '\n'


class Response(LogEntry):
    def __init__(self, bot, cmd, data):
        LogEntry.__init__(self)
        self.bot = bot
        self.cmd = cmd

        if cmd == utils.Command.SEND_FILE:
            # don't log files
            self.data = "<file>"
        else:
            self.data = data

    def __repr__(self):
        return "RESPONSE: " + str(self.timestamp) + '\n' \
            + "  bot: " + str(self.bot) + '\n' \
            + "  cmd: " + self.cmd.name + '\n' \
            + "  data: \"" + self.data + '\"\n'
