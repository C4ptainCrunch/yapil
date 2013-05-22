import socket
from spool import coroutine

class Client(object):

    def __init__(self, host=None, port=6667, nick=None, realname=None):
        self.loop = loop(host,port,nick,realname)

    def __del__(self):
        print "I am being deleted"
        self.loop.close()

    def sendraw(self,data):
        '''Send a string followed by a newline into the socket'''
        self.loop.put('{}\r\n'.format(data.strip()))

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


@coroutine
def loop(host,port,nick,realname):
    master = coroutine.self()
    mysocket = socket.create_connection((host, port))

    mysocket.send("NICK {}\r\n".format(nick))
    mysocket.send("USER {} {} bla :{}\r\n".format(nick, host, realname))

    stream = streamize(mysocket, master)

    for line in stream:

        event = tokenize(line)
        if line == 'QUIT':
            mysocket.send('QUIT :{}\r\n'.format('quiting'))
        elif event['command'] == 'PING':
            msg = ''.join(event['args'])
            #self.pong(msg)
            mysocket.send('PONG %s' % msg)
        elif event['command'] == 'ERROR':
            print(event)
            break
        put = master.get()
        if put:
            mysocket.send(put)

    mysocket.close()


def tokenize(data):
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

def streamize(socket, master):
    buffer = ''
    while master.alive():
        buffer += socket.recv(4096)
        pivot = buffer.find('\r\n')
        while pivot >= 0:
            data = buffer[:pivot]
            buffer = buffer[pivot + 2:]
            yield data
            pivot = buffer.find('\r\n')
