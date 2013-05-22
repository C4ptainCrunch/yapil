#!/usr/bin/python -O

from yapil import Client

client = Client(host='irc.freenode.net',nick='yapil-test')
client.privmsg('C4ptainCrunch', 'Coucou !')
