from socket import socket, AF_INET, SOCK_STREAM

class Client(object):

    def __init__(self, host=None, port=6667, nick=None, realname=None):
        self.host = host
        self.port = port
        self.nick = nick
        self.realname = realname
        self.socket = None
        self.buffer = ''
        self.socket_alive = False

    def connect(self):
        self.socket_alive = True
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.sendraw("NICK {}".format(self.nick))
        self.sendraw("USER {} {} bla :{}".format(self.nick, self.host, self.realname))
        try:
            self.loop()
        except (KeyboardInterrupt, SystemExit, IRCerror):
            print "\n"+"Recieved end signal. Exiting"
            self.close('Quitting')

    @property
    def stream(self):
        while self.socket_alive:
            self.buffer += self.socket.recv(1024)
            pivot = self.buffer.find('\r\n')
            while pivot >= 0:
                data = self.buffer[:pivot]
                self.buffer = self.buffer[pivot + 2:]
                yield data
                pivot = self.buffer.find('\r\n')

    def sendraw(self,data):
        self.socket.send('{}\r\n'.format(data.strip()))

    def close(self,message):
        self.sendraw('QUIT :{}'.format(message))
        # TODO : The server acknowledges this
        # by sending an ERROR message to the client.
        self.socket.close()
        self.socket_alive = False

    def pong(self, data):
        self.sendraw('PONG %s' % data)

    def join(chan,passord=''):
        self.sendraw('JOIN {} {}'.format(chan,password))

    def leave(chan,reason=''):
        self.sendraw('PART {} {}'.format(chan,reason))

    def topic(chan,topic=None):
        if topic:
            topic = ':'+topic
        self.sendraw('TOPIC {} {}'.format(chan,topic))

    def privmsg(self, recipient, message):
        self.sendraw('PRIVMSG {} :{}'.format(recipient, message))

    def talk(self, chan, message):
        self.sendraw('PRIVMSG {} :{}'.format(recipient, message))

    def loop(self):
        for line in self.stream:
            event = self.tokenize(line)
            print event
            if event['command'] == 'PING':
                msg = ''.join(event['args'])
                self.pong(msg)
            elif 'End of /MOTD command' in event['args'][1]:
                print('Realy connected')
            elif event['command'] == 'PRIVMSG':
                nick = event['prefix'].split('!', 1)[0]
                where = event['args'][0]
                msg = event['args'][1]
                self.privmsg(nick,'PONG '+msg)
            elif event['command'] == 'ERROR':
                print(event)
                raise IRCerror(event)

    def tokenize(self, data):
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
            'args' : args
            }

class IRCerror(BaseException):
    pass