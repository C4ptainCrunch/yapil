from async import go
from mainloop import create_connection
from client import MasterClient

def connect(host=None, port=6667, nick=None, realname=None, timeout=0.2):
    pipe =  go(create_connection)(host,port,nick,realname,timeout)
    client = MasterClient(pipe)
    client.wait_for_connection()
    return client