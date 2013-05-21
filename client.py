import irct0

def handler(client,event):
    print event
    if event == 'PRIVMSG':
        client.privmsg('C4ptainCrunch','caca')

irc = irct0.IRC(host='irc.freenode.net',nick='proutbot')
irc.loop(handler)