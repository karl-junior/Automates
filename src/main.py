import os
from automate import Automate  # On importe ta classe


def menu_principal():
    while True:
        # On demande le numéro de l'automate ou 'q' pour quitter
        choix = input("Quel automate voulez-vous utiliser ? tapez un chiffre entre 1 et 44  ou 'q' pour quitter : ")

        if choix.lower() == 'q': #fermeture si le choix est q
            print("Fermeture du programme. ")
            break

        nom_fichier = f"tests/automate{choix}.txt"

        # On vérifie si le fichier existe avant de le lire
        if not os.path.exists(nom_fichier):
            print(f"Erreur : Le fichier '{nom_fichier}' n'existe pas dans le dossier.")
            continue  # Retourne au début de la boucle pour redemander

        # --- LECTURE ET AFFICHAGE ---
        print(f"\n--- Chargement de l'automate numéro {choix} ---")
        mon_automate = Automate()
        mon_automate.lire_fichier(nom_fichier)
        mon_automate.afficher()

        # --- ANALYSE  ---

        # mon_automate.est_deterministe()
        # mon_automate.est_complet()

        # --- RECONNAISSANCE DE MOTS ---

        while True:
            mot = input("\nEntrez un mot à tester ou tapez 'fin' pour changer d'automate : ")
            if mot.lower() == 'fin':
                break  # Casse la boucle des mots, mais reste dans la boucle des automates


            # resultat = mon_automate.reconnaitre_mot(mot)
            # print(f"Le mot '{mot}' est-il reconnu ? {resultat}")
            print(f"(Test du mot '{mot}' à implémenter plus tard...)")



if __name__ == "__main__":
    menu_principal()
