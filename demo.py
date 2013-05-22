# Exemples de ce à quoi j'aimerais arriver à faire avec ma lib

def race(client):
    client.say('#urlab','Qui est le plus rapide ?')
    for response in client.listen('#urlab'):
        if response.text = 'Moi !':
            client.say('C\'est '+response.user)
            break

