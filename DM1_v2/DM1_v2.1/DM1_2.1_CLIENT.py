# -*- coding: utf-8 -*-
''' Félix LADISLAS, 02/10/22
    DM1, jeu de l'allumette, version 2.0 [CLIENT]
'''

############### [ importation des modules ] #####################

import socket
import threading

##### [ déclaration des constantes pour la communication ] ######

HEADER = 64                                                      #nombre de bits aloués à la déclaration de la quantité de mémoire d'un message
PORT = 5050                                                      #port de communication
SERVER = str(input("Adresse du serveur : "))                     #récupération de l'IPv4 du serveur
ADDR = (SERVER, PORT)                                            #stockage de l'IPv4 et du port pour socket
FORMAT = 'utf-8'                                                 #format d'encodage 8 bit

############## [ création du client socket] ######################

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #création du client(type de communication, flux de données)
client.connect(ADDR)                                               #connection du client à l'adresse du serveur

################ [ procédures d'affichage ] #######################

def afficheA(n):
    #affiche n fois "|"

    a = " | "
    b = a * n
    print(f"\n{b}\n")

############## [ procédure d'envoi de donnée] ######################

def send(msg):
    #procédure d'envoi d'un message (msg) au serveur

    msg = str(msg)
    message = msg.encode(FORMAT)                                      #encodage en utf-8 du message
    msg_length = len(message)                                         #récupération de la longueur du message
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))                
    client.send(send_length)                                          #envoi de la longueur du message
    client.send(message)                                              #envoi du message

#######################################################################################
#[ procédure de reception de donée et d'interprétation de donnée / jeu des allumettes]#
#######################################################################################

def receive():
    #réception et actions avec le serveur socket. Jeu des allumettes.

    nbA = 0
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)                                          #reception de la longueur du message entrant
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            
            if msg.find("!NAME") == 0:                                                           #si le message reçu commence par "!NAME"
                serverName = msg[len("!NAME"):msg.find("!END")]                                  #récupération du nom de l'adversaire

            if msg.find("!NBA") == 0:                                                                #si le message reçu commence par "!NBA"
                tour = True                                                                          #début du tour
                while tour:
                    nbA = int(msg[len("!NBA"):msg.find("!END")])                                     #actualisation du nombre d'allumettes
                    print(f"\nIl y a {nbA} allumettes.")                                             #affichage du nombre d'allumettes
                    afficheA(nbA)
                    
                    e = int(input("Combien d'allumettes souhaitez-vous retirer ? (1,2 ou 3) : "))    #tour du joueur
                    
                    if e == 1 or e == 2 or e == 3:                                                   #vérification de l'entrée du joueur
                        
                        nbA -= e                                                                     #modification du nombre d'allumettes

                        if nbA <= 0:                                                                 #vérification de la condition de victoire
                            send("!WIN")                                                             #envoi à l'adversaire que ce joueur est vainqueur
                            print("Vous avez gagné !!!")
                            input("")
                            quit()

                        send(f"!NBA{nbA}!END")                                                        #envoi à l'adversaire que ce joueur est vainqueur
                        print(f"Il y a {nbA} allumettes.")                                            #affichage du nombre d'allumettes
                        afficheA(nbA)
                        print(f"C'est à {serverName} de jouer.")                                     #tour de l'adversaire
                        tour = False                                                                 #fin du tour de ce joueur
                    else:
                        print(f"Il est impossible de retirer {e} allumettes.")


            if msg.find("!WIN") == 0:                                                             #si le message est "!WIN"
                print(f"{serverName} à gagné !!")                                                 #affichage du nom du vainqueur

################# [ programme principal ] #########################

print("\nBienvenue sur le jeu des allumettes !!\nDéveloppé par Félix LADISLAS.\n")
playerName = str(input("Entrez votre nom : "))         #nom de ce joueur

receiveThread = threading.Thread(target = receive)     #création puis lancement du thread de reception
receiveThread.start()

send(f"!NAME{playerName}!END")                         #envoi du nombre d'allumettes à l'adversaire

