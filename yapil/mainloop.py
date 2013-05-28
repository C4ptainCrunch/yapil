from helpers import eventize
from async import go
import handlers
import socket
import messages
import Queue

def create_connection(pipe, host, port, nick, realname, timeout):
    Connection(pipe, host, port, nick, realname, timeout)

class Connection(object):
    def __init__(self, pipe, host, port, nick, realname, timeout):
        self.pipe = pipe

        ping_listener = self.make_listener(handlers.ping)
        self.listeners = [pipe, ping_listener]

        self.host = host
        self.port = port
        self.nick = nick
        self.realname = realname
        self.timeout = timeout

        self.initialize()

    def initialize(self):
        self.socket = socket.create_connection((self.host, self.port), self.timeout)
        self.socket.send("NICK {}\r\n".format(self.nick))
        self.socket.send("USER {} {} bla :{}\r\n".format(self.nick, self.host, self.realname))
        self.buffer = ''

        self.loop()

    def loop(self):
        while True:
            try:
                self.recv_lines()
            except socket.timeout:
                pass
            try:
                cont = self.handle_incomming()
                if not cont:
                    break
            except Queue.Empty:
                pass
        self.socket.close()

    def recv_lines(self):
        self.buffer += self.socket.recv(1024)
        pivot = self.buffer.find('\r\n')
        while pivot >= 0:
            data = self.buffer[:pivot]
            self.buffer = self.buffer[pivot + 2:]
            print data
            self.handle_line(data)
            pivot = self.buffer.find('\r\n')

    def handle_line(self, line):
        event = eventize(line)
        if event:
            for pipe in self.listeners:
                pipe.out.put(event)

    def handle_incomming(self):
        message = self.pipe.incomming.get(block=False)

        if isinstance(message,messages.Quit):
            return False
            # TODO : get (with timeout?) one more message after
            # SIGSTOP for the QUIT message

        elif isinstance(message,messages.SendToServer):
            self.send_line(message.raw_string)

        elif isinstance(message,messages.AddListener):
            self.listeners.append(make_listener(message.fn,pipe))

        elif isinstance(message, messages.AddLogger):
            pass

        return True

    def send_line(self, line):
        success = False
        while not success:
            try:
                self.socket.send(line)
                success = True
            except socket.timeout:
                pass

    def make_listener(self, fn):

        def new_thread_fn(pipe, fn):
            from client import Client
            client = Client(pipe)
            fn(client)

        pipe = go(new_thread_fn, from_child=self.pipe.incomming, to_child=Queue.Queue())(fn)
        return pipe