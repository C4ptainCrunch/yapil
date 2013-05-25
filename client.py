#!/usr/bin/python -O

import yapil; client = yapil.client(host='irc.freenode.net',nick='yapil-test')

client.say('C4ptainCrunch', 'Coucou ')

del client
