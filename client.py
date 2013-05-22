#!/usr/bin/python -O

from yapil import Client

def plop(client):
    client.say('#urlab','Qui est le plus rapide ?')
    for response in client.listen('#urlab'):
        if response.text == 'Moi !':
            client.say("C\'est {} le plus rapide !".format(response.user))
            break

client = Client(host='irc.freenode.net',nick='yapil-test')
client.connect()

#client.add_listener(plop)