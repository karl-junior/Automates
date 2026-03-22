# Creation de la classe Automate
class Automate:

    # definition de la fonction de lecture
    def lire_fichier(self, chemin_fichier):
        try:
            with open(chemin_fichier, "r") as fichier:
                automate = fichier.readlines()

                # initialisation du nombre de symboles de l'alphabet
                self.num_symbols = int(automate[0].strip())

                # initialisation du nombre d'etats
                self.num_states = int(automate[1].strip())

                # etats initiaux (Correction : on convertit tout en entiers avec int())
                initial_line = automate[2].strip().split()
                self.num_initial_states = int(initial_line[0])
                self.initial_states = [int(x) for x in initial_line[1:]]

                # etats finaux (Correction : on convertit tout en entiers)
                final_line = automate[3].strip().split()
                self.num_final_states = int(final_line[0])
                self.final_states = [int(x) for x in final_line[1:]]

                # initialisation du nombre de transitions
                self.num_transitions = int(automate[4].strip())

                # transitions (dictionnaire)
                # clé = (état de depart, symbole) = liste d'etats d'arrivée
                self.transitions = {}

                if self.num_transitions != 0:
                    for i in range(5, 5 + self.num_transitions):
                        line = automate[i].strip()

                        # on cherche où s'arrête l'etat de depart
                        j = 0

                        # CORRECTION : On indente tout ce bloc à l'intérieur de la boucle 'for'
                        while j < len(line) and line[j].isdigit():
                            j += 1

                        # extraction de l'etat de depart
                        debut = int(line[:j])

                        # extraction du symbole de transition (j'ai corrigé la faute de frappe)
                        symbole = line[j]

                        # extraction de l'etat d'arrivée
                        fin = int(line[j + 1:])

                        # creation de la clé (etat de depart, symbole)
                        key = (debut, symbole)

                        # si la clé n'existe pas, on initialise
                        if key not in self.transitions:
                            self.transitions[key] = []

                        # ajout de l'etat d'arrivée à la liste des transitions
                        self.transitions[key].append(fin)

        except FileNotFoundError:
            print(f"Erreur : le fichier '{chemin_fichier}' n'existe pas.")

    def afficher(self):
        # genere l'alphabet
        alphabet = [chr(ord('a') + i) for i in range(self.num_symbols)]

        # Préparation des données de chaque ligne
        lignes = []
        for etat in range(self.num_states):
            # precise si c'est un etat entree ou sortie
            marqueur = ""
            if etat in self.initial_states:
                marqueur += "E "
            if etat in self.final_states:
                marqueur += "S"

            # Récupération des transitions pour cet état
            destinations_par_symbole = []
            for symbole in alphabet:
                cle = (etat, symbole)
                if cle in self.transitions:
                    # S'il y a plusieurs destinations, on les sépare par des virgules
                    dests = ",".join(str(d) for d in self.transitions[cle])
                    destinations_par_symbole.append(dests)
                else:
                    # S'il n'y a pas de transition, on met un tiret
                    destinations_par_symbole.append("--")

            # On sauvegarde la ligne : (Marqueur, Etat, Liste des destinations)
            lignes.append((marqueur.strip(), str(etat), destinations_par_symbole))

        #  Calcul de la largeur des colonnes

        largeurs_colonnes = [len(symbole) for symbole in alphabet]  # largeur d'une lettre

        # On vérifie si le contenu des cellules est plus large que l'en-tête
        for ligne in lignes:
            colonnes_etat = ligne[2]
            for i in range(len(alphabet)):
                if len(colonnes_etat[i]) > largeurs_colonnes[i]:
                    largeurs_colonnes[i] = len(colonnes_etat[i])

        # Affichage final
        print("\n======== AUTOMATE ===========")
        print(f"États initiaux : {self.initial_states}")
        print(f"États terminaux : {self.final_states}\n")

        # Affichage de l'en-tête du tableau
        # :<5 pour aligner à gauche sur 5 espaces"
        en_tete = f"{'':<5} | "
        for i, symbole in enumerate(alphabet):
            en_tete += f"{symbole:<{largeurs_colonnes[i]}} | "
        print("-" * len(en_tete))
        print(en_tete)
        print("-" * len(en_tete))  # Ligne de séparation horizontale

        # Affichage du contenu
        for marqueur, etat, colonnes_etat in lignes:
            # On place le marqueur (E/S) et le numéro de l'état
            ligne_str = f"{marqueur:<3} {etat:<1} | "

            # On place chaque destination avec la bonne largeur de colonne
            for i, dest in enumerate(colonnes_etat):
                ligne_str += f"{dest:<{largeurs_colonnes[i]}} | "

            print(ligne_str)
        print("===============================\n")

    def standardiser(self):
        return

    def est_standard(self):
        return

    def determiniser(self):
        start_state = frozenset(self.initial_states)

        new_states = [start_state]
        new_transitions = {}
        new_final_states = []

        queue = [start_state]

        while queue:
            current_set = queue.pop(0)
            
            # Si l'un des états d'origine dans ce set est terminal, le nouveau set l'est aussi
            if any(s in self.final_states for s in current_set):
                if current_set not in new_final_states:
                    new_final_states.append(current_set)
            
            # Pour chaque symbole de l'alphabet (0, 1, ..., num_symbols-1)
            for symbol in range(self.num_symbols):
                # On cherche tous les états atteignables avec ce symbole depuis le set actuel
                next_set = set()
                for state in current_set:
                    # On récupère les transitions correspondantes
                    # (Hypothèse : self.transitions est une liste de triplets (dep, sym, arr))
                    for dep, sym, arr in self.transitions:
                        if dep == state and sym == str(symbol): # Adapté selon ton format de fichier
                            next_set.add(arr)
                
                if next_set:
                    target_set = frozenset(next_set)
                    # Enregistrer la transition
                    new_transitions[(current_set, symbol)] = target_set
                    
                    # Si c'est un nouvel état découvert, on l'ajoute à la file
                    if target_set not in new_states:
                        new_states.append(target_set)
                        queue.append(target_set)

        # 3. Conversion des frozensets en entiers pour recréer un objet Automaton
        # (Optionnel : pour garder la structure propre avec des numéros d'états)
        mapping = {state: i for i, state in enumerate(new_states)}
        
        final_transitions = []
        for (src, sym), dest in new_transitions.items():
            final_transitions.append((mapping[src], str(sym), mapping[dest]))
            
        final_initials = [mapping[start_state]] if start_state else []
        final_finals = [mapping[s] for s in new_final_states]

        return Automaton(
            self.num_symbols,
            len(new_states),
            final_initials,
            final_finals,
            len(final_transitions),
            final_transitions
        )

        return

    def est_deterministe(self):
        # verification du nombre d'etats initial
        if (self.num_initial_states > 1):
            return False

        # Verification d'une unique transition pour chaque couple (etat, symbole)
        for key in self.transitions:
            if len(self.transitions[key]) > 1:
                return False
        return True

    def completer(self):
        return

    def est_complet(self):
        return

    def minimiser(self):
        return

    def est_minimal(self):
        return

    def reconnaitre_mots(self):
        return

    def automate_complementaire(self):
        return
