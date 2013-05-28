#!/usr/bin/python -O

import yapil

client = yapil.connect(host='irc.freenode.net',nick='yapil-test')
client.say('C4ptainCrunch', 'Coucou ')

import pdb
pdb.set_trace()
