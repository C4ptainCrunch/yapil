class Message:
    pass

class AddListener(Message):
    def __init__(self, fn):
        self.fn = fn

    def __str__(self):
        return '<Message(AddListener) fn at adress : {}>'.format(id(self.fn))


class SendToServer(Message):
    def __init__(self, raw_string):
        self.raw_string = '{}\r\n'.format(raw_string)

    def __str__(self):
        return '<Message(SendToServer)  : {}>'.format(self.raw_string[:-2])

class AddLogger(Message):
    def __init__(self, logger):
        self.logger = logger

    def __str__(self):
        return '<Message(AddLogger)>'

class Quit(Message):
    def __init__(self, quit_message=''):
        self.quit_message = quit_message

    def __str__(self):
        return '<Message(Quit)>'
