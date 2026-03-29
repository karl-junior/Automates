import os
from automate import Automate



def menu_principal():
    while True:
        # Choix de l'automate
        print("\n" + "="*40)
        choix = input("Quel automate voulez-vous utiliser ? (1 à 44) ou 'q' pour quitter : ")

        if choix.lower() == 'q':
            print("Fermeture du programme.")
            break

        nom_fichier = f"./tests/automate{choix}.txt"

        # Vérification de l'existence du fichier
        if not os.path.exists(nom_fichier):
            print(f"Erreur : Le fichier '{nom_fichier}' n'existe pas dans le dossier 'tests/'.")
            continue

        # Chargement et affichage
        mon_automate = Automate()
        mon_automate.lire_fichier(nom_fichier)
        
        print(f"\n--- Structure de l'automate n°{choix} ---")
        mon_automate.afficher()

        # Determinisation
        det_rep= input("Souhaitez vous déterminiser l'automate ? (oui ou non ) ")
        if det_rep.lower() == 'oui':
            if mon_automate.est_deterministe() :
                print(" Cet automate est déjà déterministe")
            else :
                mon_automate = mon_automate.determiniser()
                print("\n Automate après déterminisation :")
                mon_automate.afficher()
        if det_rep.lower() == 'non':
            print("D'accord")


        #Completer

        comp_choix= input("Souhaitez vous completer cet automate ? (oui ou non )")
        if comp_choix.lower() == 'oui':
            mon_automate.completer()
            print("Voici l'automate complété : ")
            mon_automate.afficher()

        if comp_choix.lower() == 'non':
            print("D'accord")

        # Minimiser

        mini_choix= input("Souhaitez vous minimiser cet automate ? (oui ou non )")
        if mini_choix.lower() == 'oui':
            print("L'automate doit être déterministe et complet pour cette étape : ")
            if mon_automate.est_deterministe() :
                print("L'automate est déterministe, nous pouvons continuer")
            elif not mon_automate.est_deterministe() :
                det_min_choix = input("L'automate n'est pas déterministe, souhaitez vous déterminiser cet automate ? (oui ou non) " )
                if det_min_choix.lower() == 'oui':
                    mon_automate = mon_automate.determiniser()
                    print(" C'est fait !")
                else :
                    print("Pas de minimisation possible, aurevoir")
                    break

            if not mon_automate.est_complet() :
                min_comp_choix = input("L'automate n'est pas complet, souhaitez vous compléter l'automate pour continuer ")
                if min_comp_choix.lower() == 'oui':
                    mon_automate.completer()
                else :
                    print("Pas de minimisation possible, aurevoir")
                    break

            elif mon_automate.est_complet():
                print("L'automate est minimisé nous pouvons continuer")
                mon_automate = mon_automate.minimiser()
                print( " L'automate minimisé : ")
                mon_automate.afficher()
        else :
            print("D'accord")


        choix_recherche=input("Souhaitez vous rechercher un mot dans l'automate ? (oui ou non )")

        if choix_recherche.lower() == 'oui':
            mot = input("Entrez un mot à tester ou 'c' pour changer d'automate : ")
            resultat = mon_automate.reconnaitre_mot(mot)
            if resultat:
                print(f" Le mot '{mot}' est reconnu.")
            else:
                print(f" Le mot '{mot}' n'est pas reconnu.")

            if mot.lower() == 'c':
                continue


        else :
            print("D'accord, aurevoir !")

if __name__ == "__main__":
    menu_principal()