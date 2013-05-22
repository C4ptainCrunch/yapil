#!/usr/bin/python -O

from yapil import Client

client = Client(host='irc.freenode.net',nick='yapil-test')

client.say('C4ptainCrunch', 'Coucou ')

del client
