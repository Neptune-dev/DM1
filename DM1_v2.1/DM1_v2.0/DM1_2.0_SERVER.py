# -*- coding: utf-8 -*-
''' Félix LADISLAS, 02/10/22
    DM1, jeu de l'allumette, version 2.0 [SERVER]
'''

############### [ importation des modules ] #####################

import socket
import threading

##### [ déclaration des constantes pour la communication ] ######

HEADER = 64                                                        #nombre de bits aloués à la déclaration de la quantité de mémoire d'un message
PORT = 5050                                                        #port de communication
SERVER = socket.gethostbyname(socket.gethostname())                #récupération de l'IPv4 du serveur
ADDR = (SERVER, PORT)                                              #stockage de l'IPv4 et du port pour socket
FORMAT = 'utf-8'                                                   #format d'encodage 8 bit

############## [ création du server socket] #######################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #création du serveur(type de communication, flux de données)
server.bind(ADDR)                                                  #affectation du serveur à l'addresse

################ [ procédures d'affichage ] #######################

def afficheA(n):
    #affiche n fois "|"

    a = " | "
    b = a * n
    print(f"\n{b}\n")

############## [ procédure d'envoi de donnée] ######################

def sendTo_Client(msg, conn, addr):
    #procédure d'envoi d'un message (msg) au client socket (conn) d'adresse (addr)

    msg = str(msg)
    message = msg.encode(FORMAT)                                    #encodage en utf-8 du message
    msg_length = len(message)                                       #récupération de la longueur du message
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)                                          #envoi de la longueur du message
    conn.send(message)                                              #envoi du message

#######################################################################################
#[ procédure de reception de donée et d'interprétation de donnée / jeu des allumettes]#
#######################################################################################

def handle_client(conn, addr):
    #réception et actions avec le client socket (conn) d'adresse (addr). Jeu des allumettes.

    nbA = int(input("Nombre d'allumettes de départ : "))                                        #nombre d'allumettes en jeu
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)                                           #reception de la longueur du message entrant
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg.find("!NAME") == 0:                                                          #si le message reçu commence par "!NAME"
                clientName = msg[len("!NAME"):msg.find("!END")]                                 #récupération du nom de l'adversaire
                print(f"{clientName} sera votre adversaire.")

                sendTo_Client(f"!NAME{playerName}!END", conn, addr)                             #envoi du nom du joueur à l'adveraire

                sendTo_Client(f"!NBA{nbA}!END", conn, addr)                                     #envoi du nombre d'allumettes à l'adversaire
                
                print(f"\nIl y a {nbA} allumettes.")                                            #premier affichage du nombre d'allumettes
                afficheA(nbA)
                print(f"C'est à {clientName} de jouer.")
                
            if msg.find("!NBA") == 0:                                                           #si le message reçu commence par "!NBA"
                nbA = int(msg[len("!NBA"):msg.find("!END")])                                    #actualisation du nombre d'allumettes
                print(f"\nIl y a {nbA} allumettes.")                                            #affichage du nombre d'allumettes
                afficheA(nbA)
                
                e = int(input("Combien d'allumettes souhaitez-vous retirer ? (1,2 ou 3) : "))   #tour du joueur

                nbA -= e                                                                        #modification du nombre d'allumettes

                if nbA <= 0:                                                                    #vérification de la condition de victoire
                    sendTo_Client("!WIN", conn, addr)                                           #envoi à l'adversaire que ce joueur est vainqueur
                    print("Vous avez gagné !!!")
                    input("")
                    quit()

                sendTo_Client(f"!NBA{nbA}!END", conn, addr)                                     #envoi de la nouvelle quantité d'allumettes
                print(f"Il y a {nbA} allumettes.")                                              #affichage du nombre d'allumettes
                afficheA(nbA)
                print(f"C'est à {clientName} de jouer.")                                        #tour de l'adversaire

            if msg.find("!WIN") == 0:                                                           #si le message est "!WIN"
                print(f"{clientName} à gagné !!")                                               #affichage du nom du vainqueur
                

############## [ procédure de démarage du serveur ] ##############

def start():
    #procédure de démarage du serveur

    server.listen()                                                                           #ouverture du serveur
    print(f"[LISTENING] Le serveur recherche une connection sur {SERVER}")
    while True:
        conn, addr = server.accept()                                                          #récupération de l'addresse du client nouvellement connecté
        handleThread = threading.Thread(target = handle_client, args = (conn, addr))          #création puis lancement du thread principal
        handleThread.start()

################# [ programme principal ] #########################

print("\nBienvenue sur le jeu des allumettes !!\nDéveloppé par Félix LADISLAS.\n")

playerName = str(input("Entrez votre nom : "))                      #nom de ce joueur

print("\n[STARTING] le serveur démarre...")

start()                                                             #démarage du serveur
