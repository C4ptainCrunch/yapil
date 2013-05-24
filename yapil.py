import socket
from spool import coroutine
from time import sleep

class Client(object):

    def __init__(self, host=None, port=6667, nick=None, realname=None, timeout=0.2):
        self.handlers = []
        self.loop = loop(host,port,nick,realname,timeout)
        # TODO : make __init__ blocking untill connection is established

    def __del__(self):
        print "SIGSTOP signal sent, waiting for children to die"
        self.loop.put('SIGSTOP')


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

    def say(self, nick):
        self.sendraw('NICK {}'.format(nick))



@coroutine
def loop(host,port,nick,realname,timeout):
    master = coroutine.self()

    try:
        mysocket = socket.create_connection((host, port),timeout)

        mysocket.send("NICK {}\r\n".format(nick))
        mysocket.send("USER {} {} bla :{}\r\n".format(nick, host, realname))
        # TODO : make connexion detection and throw an event
        # wait for a [001-004] numeric response and send events
        # see http://tools.ietf.org/html/rfc2812#section-5.1

        buffer = ''
        send = None

        while True:
            try:
                buffer += mysocket.recv(1024)
                pivot = buffer.find('\r\n')
                while pivot >= 0:
                    data = buffer[:pivot]
                    buffer = buffer[pivot + 2:]
                    handle_line(data,mysocket)
                    pivot = buffer.find('\r\n')
            except socket.timeout:
                pass

            try:
                if not send:
                    send = master.get(block=False)
                if send == 'SIGSTOP':
                    # TODO : get (with timeout?) one more message after SIGSTOP for the QUIT message
                    break
                elif send:
                    mysocket.send(send)
                    send = None
            except socket.timeout:
                pass

    except Exception:
        raise
    finally:
        mysocket.close()


def handle_line(line,mysocket):
    # TODO : get rid of mysocket param and use the Client API
    print line
    event = tokenize(line)
    # TODO : send events to a thread to be treated
    if event['command'] == 'PING':
        msg = ''.join(event['args'])
        mysocket.send('PONG %s' % msg)
    elif event['command'] == 'PRIVMSG':
        pass
    elif event['command'] == 'ERROR':
        print 'Error !  '



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