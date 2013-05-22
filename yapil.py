import socket
from spool import coroutine
from time import sleep

class Client(object):

    def __init__(self, host=None, port=6667, nick=None, realname=None):
        self.loop = loop(host,port,nick,realname)
        # TODO : make __init__ blocking untill connection is established

    def __del__(self):
        print "Queue is beeing emptied..."
        # TODO : wait untill queue is empty instead of sleep
        sleep(20)
        print "Stoping loop"
        self.loop.close()
        print "Bye"

    def sendraw(self,data):
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

    def say(self, recipient, message):
        '''Send a message to a user/channel'''
        self.sendraw('PRIVMSG {} :{}'.format(recipient, message))



@coroutine
def loop(host,port,nick,realname):
    master = coroutine.self()
    mysocket = socket.create_connection((host, port))

    mysocket.send("NICK {}\r\n".format(nick))
    mysocket.send("USER {} {} bla :{}\r\n".format(nick, host, realname))
    # TODO : replace sleep by better connexion detection
    sleep(10)
    stream = streamize(mysocket, master)

    for line in stream:

        event = tokenize(line)
        if line == 'QUIT':
            mysocket.send('QUIT :{}\r\n'.format('quiting'))
        elif event['command'] == 'PING':
            msg = ''.join(event['args'])
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
