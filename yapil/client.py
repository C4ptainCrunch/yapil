import handlers
import events
import messages

class Client(object):
    def __init__(self, pipe):
        self.pipe = pipe

    @property
    def events(self):
        while True:
            yield self.pipe.incomming.get()

    def listen_ping(self):
        for event in self.events:
            if isinstance(event, events.Ping): yield event

    def listen_private(self):
        for event in self.events:
            if isinstance(event, events.Privmsg):
                yield event


    def pong(self, data):
        '''Sends a pong to the server'''
        self.to_server('PONG %s' % data)

    def join(self, chan,password=''):
        '''Join a chan'''
        self.to_server('JOIN {} {}'.format(chan,password))

    def leave(self, chan,reason=''):
        '''Leave a chan'''
        self.to_server('PART {} {}'.format(chan,reason))

    def topic(self, chan,topic=''):
        '''Ask for the current topic or set it (if topic!='')'''
        if topic:
            topic = ':'+topic
        self.to_server('TOPIC {} {}'.format(chan,topic))

    def say(self, recipient, message):
        '''Send a message to a user/channel'''
        self.to_server('PRIVMSG {} :{}'.format(recipient, message))

    def action(self,recipient, message):
        self.say(recipient,'\x01ACTION '+message)

    def nick(self, nick):
        self.to_server('NICK {}'.format(nick))


    def send_to_loop(self,obj):
        self.pipe.out.put(obj)

    def to_server(self,data):
        self.send_to_loop(messages.SendToServer(data))

    def add_listener(self,fn):
        self.send_to_loop(messages.AddListener(fn))

    def set_logger(self,logger):
        self.send_to_loop(messages.AddLogger(logger))


class MasterClient(Client):

    def __del__(self):
        print "Die sponge, die!"
        # TODO send die message

    def wait_for_connection(self):
        num_rply = [False]*4
        for event in self.events:
            if isinstance(event, events.NumericReply):
                if 0 <= event.numeric <= 4:
                    num_rply[event.numeric-1] = True
            if reduce(lambda a,b: a and b,num_rply):
                break
        return event.server
