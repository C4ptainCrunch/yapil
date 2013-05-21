from socket import socket, AF_INET, SOCK_STREAM

class IRC(object):

    def __init__(self, host=None, port=6667, nick=None, realname=None):
        self.host = host
        self.port = port
        self.nick = nick
        self.realname = realname
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.buffer = ''

    def connect(self):
        self.realname = self.realname or self.nick
        assert(self.host and self.port and self.nick and self.realname)
        self.socket.connect((self.host, self.port))
        self.socket.send("NICK %s\r\n" % self.nick)
        self.socket.send("USER %s %s bla :%s\r\n" % (self.nick, self.host, self.realname))

    def stream(self):
        self.buffer += self.socket.recv(1024)
        while True:
            pivot = self.buffer.find('\r\n')
            while pivot >= 0:

                if pivot >= 0:
                    data, self.buffer = (self.buffer[:pivot],
                                         self.buffer[pivot + 2:])
                    event = Event(data)
                    if event.type == 'PING':
                        self.ping(event.msg)
                    else:
                        yield Event(data)
                pivot = self.buffer.find('\r\n')
            self.buffer += self.socket.recv(1024)

    def ping(self, data):
        self.socket.send('PONG %s\r\n' % data)

    def privmsg(self, recipient, data):
        self.socket.send('PRIVMSG %s :%s\r\n' % (recipient, data))

    def close(self):
        self.socket.close()

    def communicate(self,event):
        response=Response(self)
        self.handler(response,event)

    def loop(self,handler=lambda x:None):
        self.handler = handler
        self.connect()
        for event in self.stream():
            if '.freenode.net' in event.prefix and 'End of /MOTD command' in event.args[1]:
                self.communicate('CONNECTED')
                print('Connected.')
            elif event.type == 'PRIVMSG':
                self.communicate('PRIVMSG')
                #self.privmsg(event.nick, event.msg)
            elif event.type == 'ERROR':
                print(event)
                self.close()


class Response(object):
    def __init__(self, client):
        self.client = client
    def privmsg(self,user,message):
        self.client.privmsg(user,message)

class Event(object):

    def __init__(self, data):
        """Breaks a message from an IRC server into its prefix, command, and arguments.
        """
        prefix = ''
        trailing = []
        self.data = data

        if not data:
           raise IRCBadMessage("Empty line.")
        if data[0] == ':':
            prefix, data = data[1:].split(' ', 1)
        if data.find(' :') != -1:
            data, trailing = data.split(' :', 1)
            args = data.split()
            args.append(trailing)
        else:
            args = data.split()
        command = args.pop(0)

        self.prefix, self.command, self.args = prefix, command, args
        self.type = self.command

        self.nick = None
        self.where = None
        self.msg = None

        if self.type == 'PRIVMSG':
            self.nick = self.prefix.split('!', 1)[0]
            self.where = self.args[0]
            self.msg = self.args[1]
        if self.type == 'PING':
            self.msg = ''.join(self.args)

    def __str__(self):
        return '<Event %s>' % repr((self.prefix, self.command, self.args))