class BaseEvent:
    pass

class Ping(BaseEvent):
    def __init__(self, tokenized):
        self.msg = ''.join(tokenized['args'])

class Privmsg(BaseEvent):
    def __init__(self, tokenized):
        self.nick = tokenized['prefix'].split('!', 1)[0]
        self.msg = tokenized['args'][1]

class NumericReply(BaseEvent):
    def __init__(self, tokenized):
        self.numeric = int(tokenized['command'])
        self.server = tokenized['prefix']
