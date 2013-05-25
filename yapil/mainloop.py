from spool import coroutine, go
from helpers import eventize
import handlers
import socket

@coroutine
def loop(host,port,nick,realname,timeout):
    from interface import Client

    master = coroutine.self()
    queue = master._in
    cc = Client(queue)
    go(handlers.ping)(cc)
    mysocket = socket.create_connection((host, port),timeout)
    try:
        mysocket.send("NICK {}\r\n".format(nick))
        mysocket.send("USER {} {} bla :{}\r\n".format(nick, host, realname))
        # TODO : make connexion detection and throw an event
        # wait for a [001-004] numeric response and send events
        # see http://tools.ietf.org/html/rfc2812#section-5.1
        buffer = ''
        while True:
            try:
                buffer += mysocket.recv(1024)
                pivot = buffer.find('\r\n')
                while pivot >= 0:
                    data = buffer[:pivot]
                    buffer = buffer[pivot + 2:]
                    print data
                    handle_line(data,queue,cc)
                    pivot = buffer.find('\r\n')
            except socket.timeout:
                pass
            try:
                if queue.empty():
                    continue
                line = queue.get()
                if line == 'SIGSTOP':
                    break # TODO : get (with timeout?) one more message after SIGSTOP for the QUIT message
                else:
                    mysocket.send(line)
            except socket.timeout:
                pass
    except Exception:
        raise
    finally:
        mysocket.close()


def handle_line(line,own_queue,cc):
    event = eventize(line)
    if event:
        cc.from_master.put(event)