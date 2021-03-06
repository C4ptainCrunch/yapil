import events

def eventize(line):
    tokenized = tokenize(line)
    event_type = events.BaseEvent
    if tokenized['command'].decode().isnumeric():
        event_type = events.NumericReply
    elif tokenized['command'] == 'PING':
        event_type =  events.Ping
    elif tokenized['command'] == 'PRIVMSG':
        print tokenized
        if not is_chan(tokenized['args'][0]):
            print 'returning a privmsg'
            event_type = events.Privmsg
        else:
            print 'Not handeld - chan message'

    if not event_type == events.BaseEvent:
        return event_type(tokenized)

def is_chan(name):
    return name[0] in ('&', '#', '+', '!')

def tokenize(data):
    '''Tokenize a line from the socket into : a prefix, a command and some args'''
    prefix = ''
    trailing = []

    if not data:
       return {'type' : 'empty'}
    if data[0] == ':':
        prefix, data = data[1:].split(' ', 1)
    if data.find(' :') != -1:
        data, trailing = data.split(' :', 1)
        args = data.split()
        args.append(trailing)
    else:
        args = data.split()
    command = args.pop(0)

    return {'prefix' : prefix,
        'command' : command,
        'args' : args}