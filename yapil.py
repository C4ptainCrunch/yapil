import socket
from spool import coroutine

class Client(object):

    def __init__(self, host=None, port=6667, nick=None, realname=None):
        self.host = host
        self.port = port
        self.nick = nick
        self.realname = realname

        self.child = self.connect()

    @coroutine
    def connect(self):
        parent = coroutine.self()
        self.socket = socket.create_connection((self.host, self.port))
        self.sendraw("NICK {}".format(self.nick))
        self.sendraw("USER {} {} bla :{}".format(self.nick, self.host, self.realname))
        self.loop(parent)


    @property
    def stream(self):
        self.buffer = ''
        while True:
            self.buffer += self.socket.recv(4096)
            pivot = self.buffer.find('\r\n')
            while pivot >= 0:
                data = self.buffer[:pivot]
                self.buffer = self.buffer[pivot + 2:]
                yield data
                pivot = self.buffer.find('\r\n')

    def sendraw(self,data):
        '''Send a string followed by a newline into the socket'''
        self.socket.send('{}\r\n'.format(data.strip()))

    def close(self,message):
        '''Sends a quit command and closes the socket'''
        self.sendraw('QUIT :{}'.format(message))
        # TODO : The server acknowledges this
        # by sending an ERROR message to the client.
        self.socket.close()

    def pong(self, data):
        '''Sends a pong to the server'''
        self.sendraw('PONG %s' % data)

    def join(self, chan,password=''):
        '''Join a chan'''
        self.sendraw('JOIN {} {}'.format(chan,password))

    def leave(self, chan,reason=''):
        '''Leave a chan'''
        self.sendraw('PART {} {}'.format(chan,reason))

    def topic(self, chan,topic=''):
        '''Ask for the current topic or set it (if topic!='')'''
        if topic:
            topic = ':'+topic
        self.sendraw('TOPIC {} {}'.format(chan,topic))

    def privmsg(self, recipient, message):
        '''Send a private message'''
        self.sendraw('PRIVMSG {} :{}'.format(recipient, message))

    def talk(self, chan, message):
        '''Talk on a chan'''
        self.sendraw('PRIVMSG {} :{}'.format(chan, message))

    def loop(self,parent):
        '''IRC loop : gets a line from the stream and does some things with it'''
        for line in self.stream:
            event = self.tokenize(line)
            print event
            if event['command'] == 'PING':
                msg = ''.join(event['args'])
                self.pong(msg)
            # elif 'End of /MOTD command' in event['args'][1]:
            #     print('Realy connected')
            elif event['command'] == 'ERROR':
                print(event)
                raise IRCerror(event)
            if not parent.alive():
                break

    def tokenize(self, data):
        '''Tokenize a line from the socket into : a prefix, a command and some args'''
        prefix = ''
        trailing = []

        if not data:
           return {'type' : 'empty'}
        if data[0] == ':':
            prefix, data = data[1:].split(' ', 1)
        if data.find(' :') != -1:
            data, trailing = data.split(' :', 1)
            args = data.split()
            args.append(trailing)
        else:
            args = data.split()
        command = args.pop(0)

        return {'prefix' : prefix,
            'command' : command,
            'args' : args}

class IRCerror(BaseException):
    pass