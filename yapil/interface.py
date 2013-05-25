import multiprocessing

import handlers
import events
from mainloop import loop

def connect( host=None, port=6667, nick=None, realname=None, timeout=0.2):
    loop_instance =  loop(host,port,nick,realname,timeout)
    # TODO : make __init__ blocking untill connection is established
    return Client(loop_instance)

class Client(object):
    def __init__(self, to_master):
        self.to_master = to_master
        self.from_master = multiprocessing.Queue()

    @property
    def events(self):
        while True:
            yield self.from_master.get()

    def listen_ping(self):
        for event in self.events:
            if isinstance(event, events.Ping): yield event

    def listen_private(self):
        for event in self.events:
            if isinstance(event, events.Privmsg):
                yield event

    def sendraw(self,data):
        self.to_master.put('{}\r\n'.format(data))

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

    def action(self,recipient, message):
        self.say(recipient,'\x01ACTION '+message)

    def nick(self, nick):
        self.sendraw('NICK {}'.format(nick))