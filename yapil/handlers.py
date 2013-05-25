def ping(client):
    for ping in client.listen_ping():
        client.pong(ping.msg)