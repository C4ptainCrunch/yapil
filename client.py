import irct0

def handler(client,event):
    print event
    if event == 'PRIVMSG':
        client.privmsg('C4ptainCrunch','caca')

client = irct0.Client(host='irc.freenode.net',nick='proutbot')
client.connect()