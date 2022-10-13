# -*- coding: utf-8 -*-
''' Félix LADISLAS, 01/10/22
    DM1, jeu de l'allumette, version 1.0
'''
from random import randint

################ Procédures usuelles #######################

def dessineAllumettes(nb):
    #dessine nb allumettes dans l'invite de commande.
    a = " | "
    b = nb * a
    print("\n", b, "\n")

############## Fonction du jeu ############################

def jeuAllumettes(n):
    # Effectue une partie du jeu des allumettes et retourne le nom du gagnant dans une chaine de caractère.

    print("\nJeu réalisé par Félix LADISLAS.\n")

    joueur_1 = str(input("Entrez le nom du 1er joueur : "))
    joueur_2 = str(input("Entrez le nom du 2nd joueur : "))
    
    print("\nCelui qui prend la dernière allumettes GAGNE !!!\n")

    initiative = randint(0, 1)   # On choisit au hasard le joueur qui commence en premier.

    nbAllumettes = n             # Nombre d'allumettes encore en jeu.

    while True:                  # "while true loop" qui répète les manches tant que le programme n'a pas désigné de vainqueur.

        print(f"\nIl y a {nbAllumettes} allumettes.")
        dessineAllumettes(nbAllumettes)

        r = 0 

        if initiative == 0:
            print(f"\nC'est à {joueur_1} de jouer.")
            r = int(input("\nCombien d'allumettes souhaitez vous retirer ? (1,2 ou 3) : "))
            
            nbAllumettes = nbAllumettes - r
        
            if nbAllumettes == 0:    # Si le nombre d'allumette tombe à 0 une fois que joueur_1 a joué,
                return(joueur_1)     # alors on quitte la "while loop" et la fonction en retournant joueur_1.
            else:
                initiative = 1       # on change de joueur pour le tour prochain.
    
        elif initiative == 1:
            print(f"\nC'est à {joueur_2} de jouer.")
            r = int(input("\nCombien d'allumettes souhaitez vous retirer ? (1,2 ou 3) : "))

            nbAllumettes = nbAllumettes - r
        
            if nbAllumettes == 0:    # Même fonctionnement qu'au dessus mais pour joueur_2.
                return(joueur_2)
            else:
                initiative = 0



############## Programme principal #####################


n = int(input("Combien doit-il y avoir d'allumettes ? : "))
print(f"\nLe gagnant est : {jeuAllumettes(n)} !!\n")
