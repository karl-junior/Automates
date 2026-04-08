import os
from automate import Automate

def menu_principal():
    while True:
        # SELECTION
        print("\n" + "═"*50)
        choix = input("Quel automate (1-45) ou 'q' : ")
        if choix.lower() == 'q': break

        
        chemins_possibles = [
            f"tests/automate{choix}.txt",      # Si on est dans /AUTOMATES
            f"../tests/automate{choix}.txt",   # Si on est dans /src
            f"automate{choix}.txt"             # Si le fichier est au même endroit
        ]

        nom_fichier = None
        for p in chemins_possibles:
            if os.path.exists(p):
                nom_fichier = p
                break

        if not nom_fichier:
            print(f"Erreur : Impossible de trouver 'automate{choix}.txt'")
            
            print(f"Dossier actuel : {os.getcwd()}") 
            continue

        mon_automate = Automate()
        mon_automate.lire_fichier(nom_fichier)
        
        
        # Menu du programme
        while True:
            print("\n" + "─"*30)
            print(f"ANALYSE DE L'AUTOMATE N°{choix} :")
            
            
            est_det = "OUI" if mon_automate.est_deterministe() else "NON"
            est_std = "OUI" if mon_automate.est_standard() else "NON"
            est_comp = "OUI" if mon_automate.est_complet() else "NON"
            
            print(f"Déterministe : {est_det} | Standard : {est_std} | Complet : {est_comp}")
            mon_automate.afficher()

            print("\n--- ACTIONS ---")
            print("1. Standardiser")
            print("2. Déterminiser")
            print("3. Compléter")
            print("4. Minimiser")
            print("5. Tester un mot")
            print("6. Complémentaire")
            print("c. CHANGER d'automate")
            
            action = input("\nVotre choix : ").lower()

            if action == 'c': 
                break

            elif action == '1':
                print("\nLancement de la Standardisation...")
                mon_automate.standardiser()

            elif action == '2':
                print("\nLancement de la Déterminisation...")
                mon_automate = mon_automate.determiniser()

            elif action == '3':
                print("\nLancement de la Complétion...")
                mon_automate.completer()

            elif action == '4':
                print("\nLancement de la Minimisation...")
                if not mon_automate.est_deterministe(): 
                    mon_automate = mon_automate.determiniser()
                if not mon_automate.est_complet(): 
                    mon_automate.completer()
                mon_automate = mon_automate.minimiser()

            elif action == '5': 
                print("\n--- Mode Reconnaissance de mots ---")
                print("(Tapez 'fin' pour arrêter)")
                while True:
                    mot = input("Entrez un mot à tester : ").strip()
                    if mot.lower() == 'fin':
                        print("Retour au menu principal.")
                        break
                    
                    
                    resultat = mon_automate.reconnaitre_mot(mot if mot != "£" else "")
                    
                    
                    print(f"'{mot if mot else 'mot vide'}' : {'oui' if resultat else 'non'}")

            elif action == '6':
                print("\n--- Phase de Complémentarisation ---")
                nouvel_auto = mon_automate.complementaire()
                if nouvel_auto:
                    mon_automate = nouvel_auto
                    # L'automate affiché juste après sera le complémentaire
            
            else:
                print("Choix non reconnu.")

if __name__ == "__main__":
    menu_principal()
