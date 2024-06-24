import socket
print("111")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddress = s.getsockname()[0]
s.close()
print("ip:",ipaddress)
port = 8765
# 1) création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2) liaison du socket à une adresse précise :
try:
    mySocket.bind((ipaddress, 8765))
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.", socket.error)
    sys.exit()

while 1:
    # 3) Attente de la requête de connexion d'un client :
    print("Serveur prêt, en attente de requêtes ...")
    mySocket.listen(5)

    # 4) Etablissement de la connexion :
    connexion, adresse = mySocket.accept()
    print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

    connexion.send("hello serveur".encode('utf-8'))
    msgClient = connexion.recv(1024)
    print(msgClient.decode('utf-8'))