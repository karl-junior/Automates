import os

class Automate:
    def __init__(self):
        self.num_symboles = 0
        self.num_etats = 0
        self.etats_initiaux = []
        self.num_etats_initiaux = 0
        self.etats_finaux = []
        self.num_etats_finaux = 0
        self.num_transitions = 0
        self.transitions = {}

    def lire_fichier(self, chemin_fichier):
        try:
           
            if not os.path.exists(chemin_fichier) and os.path.exists(f"tests/{chemin_fichier}"):
                chemin_fichier = f"tests/{chemin_fichier}"

            with open(chemin_fichier, "r", encoding="utf-8") as fichier:
                automate = [ligne.strip() for ligne in fichier if ligne.strip()]

            if not automate: return

            self.num_symboles = int(automate[0])
            self.num_etats = int(automate[1])

            ligne_init = automate[2].split()
            self.num_etats_initiaux = int(ligne_init[0])
            self.etats_initiaux = [int(x) for x in ligne_init[1:]]

            ligne_fin = automate[3].split()
            self.num_etats_finaux = int(ligne_fin[0])
            self.etats_finaux = [int(x) for x in ligne_fin[1:]]

            self.num_transitions = int(automate[4])
            self.transitions = {}

            for i in range(5, 5 + self.num_transitions):
                if i < len(automate):
                    p = automate[i].split()
                    if len(p) >= 3:
                        deb, sym, fin = int(p[0]), p[1], int(p[2])
                        
                        # Solution de l'epsilon "caché"
                        if sym == '£' or sym == 'epsilon': 
                            sym = '£'
                        
                        if (deb, sym) not in self.transitions:
                            self.transitions[(deb, sym)] = []
                        if fin not in self.transitions[(deb, sym)]:
                            self.transitions[(deb, sym)].append(fin)
            print(f"Fichier '{chemin_fichier}' chargé.")
        except Exception as e:
            print(f"Erreur lecture : {e}")

    def afficher(self):
        """Affiche l'automate sous forme de table de transition"""
        # 1. Extraction et nettoyage de l'alphabet
        symboles_presents = set(sym for (_, sym) in self.transitions.keys())
        
        # On définit l'alphabet réel (a, b...) en excluant l'epsilon (qu'il s'appelle £ ou c)
        alphabet = sorted([s for s in symboles_presents if s != "£" and s != "c"])
        
        # On ajoute l'epsilon à la fin si présent, en l'unifiant sous le symbole £
        has_epsilon = "£" in symboles_presents or "c" in symboles_presents
        if has_epsilon:
            alphabet.append("£")
        
        if not alphabet: 
            alphabet = [" "]

        # 2. Préparation des lignes et calcul des largeurs
        lignes = []
        # Largeur par défaut basée sur le nom du symbole
        largeurs_colonnes = [len(sym) for sym in alphabet]

        for etat in range(self.num_etats):
            marqueur = ""
            if etat in self.etats_initiaux: marqueur += "E "
            if etat in self.etats_finaux: marqueur += "S"
            
            destinations = []
            for i, symbole in enumerate(alphabet):
                # Si on cherche l'epsilon unifié £, on regarde aussi pour 'c'
                sym_recherche = symbole
                if symbole == "£" and "c" in symboles_presents:
                    sym_recherche = "c"
                
                cle = (etat, sym_recherche)
                if cle in self.transitions:
                    dests_str = ",".join(str(d) for d in sorted(self.transitions[cle]))
                else:
                    dests_str = "--"
                
                destinations.append(dests_str)
                # On ajuste la largeur de la colonne si une destination est longue (ex: 1,2,5)
                if len(dests_str) > largeurs_colonnes[i]:
                    largeurs_colonnes[i] = len(dests_str)
            
            lignes.append((marqueur.strip(), str(etat), destinations))

        # 3. Calcul de la largeur de la colonne de gauche (Marqueurs + Numéro)
        largeur_num_etat = max(len(l[1]) for l in lignes) if lignes else 1
        largeur_col_gauche = 4 + largeur_num_etat # Place pour "E S "

        # 4. Affichage final
        print("\n" + "="*20 + " TABLEAU DE TRANSITION " + "="*20)
        
        # En-tête
        en_tete = f"{'':<{largeur_col_gauche}} | "
        for i, symbole in enumerate(alphabet):
            en_tete += f"{symbole:^{largeurs_colonnes[i]}} | "
        
        print(en_tete)
        print("-" * len(en_tete))

        # Contenu des états
        for marqueur, num_etat, cols in lignes:
            # Alignement : Marqueur à gauche, numéro à droite
            label_etat = f"{marqueur:<3} {num_etat:>{largeur_num_etat}}"
            ligne_str = f"{label_etat} | "
            
            for i, dest in enumerate(cols):
                ligne_str += f"{dest:^{largeurs_colonnes[i]}} | "
            
            print(ligne_str)
        
        print("=" * len(en_tete) + "\n")

    
    def afficher_composition(self, mapping):
        """Affiche la correspondance entre les états composés et les nouveaux indices."""
        print("\nTable de correspondance des états composés (AF -> AFDC) :")
        for compose, index in mapping.items():
            # On trie les anciens états et on les sépare par un point
            liste_etats = sorted(list(compose))
            composition = "{" + ".".join(map(str, liste_etats)) + "}"
            print(f"  État {index} correspond à : {composition}")

    def est_deterministe(self, verbose=True):
        raisons = []
        
        # Un AF ne doit avoir qu'un seul état initial
        if self.num_etats_initiaux > 1:
            raisons.append(f"- Il possède {self.num_etats_initiaux} états initiaux, au lieu d'un seul.")
        
        # Un AF ne doit pas avoir d'epsilon-transitions (£)
        if self.automate_epsilon():
            raisons.append("- Il contient des epsilon-transitions (£).")
        
        # Chaque état ne doit avoir qu'une seule transition possible par symbole
        conflits = []
        for (etat, sym), successeurs in self.transitions.items():
            if len(successeurs) > 1:
                conflits.append(f"({etat}, {sym})")
        
        if conflits:
            raisons.append(f"- Transitions multiples pour les couples : {', '.join(conflits)}.")

        if raisons:
            if verbose:
                print("\nL'automate n'est PAS déterministe pour les raisons suivantes :")
                for r in raisons:
                    print(r)
            return False
        
        return True

    def determiniser(self):
        if self.est_deterministe(verbose=True):
            print("\nL'automate est déjà DÉTERMINISTE.")
            return self.completer() if not self.est_complet() else self

        print("\n--- Phase de Déterminisation (Sous-ensembles) ---")
        # On définit l'alphabet sans epsilon
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        alphabet = [s for s in alphabet if s != '£']

        start_set = self.fermeture_epsilon(self.etats_initiaux)
        new_states = [start_set]
        new_trans = {}
        queue = [start_set]

        while queue:
            current_set = queue.pop(0)
            for sym in alphabet:
                next_set_raw = set()
                for etat in current_set:
                    next_set_raw.update(self.transitions.get((etat, sym), []))
                
                if next_set_raw:
                    next_set = self.fermeture_epsilon(next_set_raw)
                    print(f"  Transition : {list(current_set)} --({sym})--> {list(next_set)}")
                    new_trans[(current_set, sym)] = next_set
                    if next_set not in new_states:
                        new_states.append(next_set)
                        queue.append(next_set)

        auto_det = Automate()
        auto_det.num_symboles = self.num_symboles
        auto_det.num_etats = len(new_states)
        mapping = {s: i for i, s in enumerate(new_states)}

        auto_det.etats_initiaux = [mapping[start_set]]
        auto_det.num_etats_initiaux = 1
        auto_det.etats_finaux = [mapping[s] for s in new_states if any(e in self.etats_finaux for e in s)]
        auto_det.num_etats_finaux = len(auto_det.etats_finaux)
        
        for (src, sym), dst in new_trans.items():
            auto_det.transitions[(mapping[src], sym)] = [mapping[dst]]
        
        # Affichage de la composition 
        self.afficher_composition(mapping)
        
        # Complétion automatique après déterminisation
        if not auto_det.est_complet():
            print("\nComplétion de l'automate déterministe...")
            auto_det.completer()
            
        return auto_det

    def est_complet(self, verbose=True):
        """Vérifie si l'automate est complet en ignorant les transitions epsilon."""
        # 1. On définit l'alphabet de test (ex: 'a', 'b')
        # On génère l'alphabet selon le nombre de symboles, mais on exclut l'epsilon
        alphabet_test = [chr(ord('a') + i) for i in range(self.num_symboles)]
        alphabet_test = [s for s in alphabet_test if s != "£" and s != "c"]
        
        raisons = []
        complet = True

        # 2. Vérification pour chaque état et chaque lettre
        for i in range(self.num_etats):
            for sym in alphabet_test:
                # Un état est incomplet s'il n'y a pas de transition pour un symbole donné
                if (i, sym) not in self.transitions or not self.transitions[(i, sym)]:
                    raisons.append(f"- État {i} n'a pas de transition pour '{sym}'")
                    complet = False

        # 3. Affichage des raisons si l'automate est incomplet
        if not complet and verbose:
            print("\nL'automate n'est PAS COMPLET :") #
            for r in raisons:
                print(r) #
        
        return complet
    
    def completer(self):
        if self.est_complet():
            print("L'automate est déjà complet.")
            return
    
        # Alphabet des lettres (a, b, c...) uniquement
        alphabet_reel = sorted(list(set(sym for (_, sym) in self.transitions.keys() if sym != "£")))
        
        poubelle = self.num_etats
        poubelle_creee = False

        for i in range(self.num_etats):
            for sym in alphabet_reel:
                if (i, sym) not in self.transitions or not self.transitions[(i, sym)]:
                    if not poubelle_creee:
                        self.num_etats += 1
                        poubelle_creee = True
                    self.transitions[(i, sym)] = [poubelle]

        if poubelle_creee:
            for sym in alphabet_reel:
                self.transitions[(poubelle, sym)] = [poubelle]
            print(f"État poubelle {poubelle} ajouté.")
        
        return self 

    def est_standard(self, verbose=True):
        raisons = []
        
        # 1. Vérification du nombre d'états initiaux
        if self.num_etats_initiaux != 1:
            raisons.append(f"- Il possède {self.num_etats_initiaux} états initiaux (il en faut exactement 1).")
        
        # 2. Vérification des transitions vers l'état initial
        if self.num_etats_initiaux == 1:
            init = self.etats_initiaux[0]
            # On cherche si 'init' est présent dans n'importe quelle liste de destinations
            for (etat_dep, sym), destinations in self.transitions.items():
                if init in destinations:
                    raisons.append(f"- L'état initial {init} est la cible d'une transition depuis l'état {etat_dep} avec '{sym}'.")
                    break # Une seule raison suffit pour dire qu'il n'est pas standard

        # 3. Affichage et retour
        if raisons:
            if verbose:
                print("\nL'automate n'est PAS STANDARD :")
                for r in raisons:
                    print(r)
            return False
        
        return True

    def standardiser(self):
        if self.est_standard():
            print("L'automate est déjà STANDARD. Opération annulée.")
            return self
        
        print(f"Création d'un nouvel état initial {self.num_etats} déconnecté de toute transition entrante.")

        # 1. Créer le nouvel état initial (index = num_etats actuel)
        new_init = self.num_etats
        print(f"\n--- Phase de Standardisation ---")
        print(f"  Action : Création d'un nouvel état initial unique (État {new_init}).")
        print(f"  Objectif : Garantir qu'aucune transition ne revient vers l'entrée.")
        
        # 2. Identifier tous les symboles (y compris £)
        alphabet_complet = set(sym for (_, sym) in self.transitions.keys())
        
        new_trans = self.transitions.copy()
        new_finaux = list(self.etats_finaux)

        # 3. Le nouvel état doit avoir les mêmes sorties que tous les anciens initiaux
        print(f"  Action : Copie des transitions des anciens initiaux {self.etats_initiaux} vers l'état {new_init}.")
        for sym in alphabet_complet:
            targets = set()
            for e_old in self.etats_initiaux:
                if (e_old, sym) in self.transitions:
                    targets.update(self.transitions[(e_old, sym)])
            
            if targets:
                new_trans[(new_init, sym)] = list(targets)

        # 4. Gérer le caractère final
        # Si un des anciens initiaux était final, le nouveau le devient
        if any(e in self.etats_finaux for e in self.etats_initiaux):
            print(f"  Note : Un ancien état initial était final, donc l'état {new_init} devient FINAL (acceptation du mot vide).")
            if new_init not in new_finaux:
                new_finaux.append(new_init)

        # 5. Mise à jour de l'objet
        self.num_etats += 1
        self.etats_initiaux = [new_init]
        self.num_etats_initiaux = 1
        self.etats_finaux = new_finaux
        self.transitions = new_trans

        print(f"  Résultat : L'automate est désormais standardisé.")
        return self

   

    def complementaire(self):
        # Affichage du type d'automate source
        type_source = "AFDCM (Minimal)" if self.est_minimal() else "AFDC (Déterministe Complet)"
        print(f"\nConstruction du complémentaire à partir de : {type_source}")

        auto_comp = Automate()
        auto_comp.num_symboles = self.num_symboles
        auto_comp.num_etats = self.num_etats
        auto_comp.etats_initiaux = list(self.etats_initiaux)
        auto_comp.num_etats_initiaux = self.num_etats_initiaux
        auto_comp.transitions = self.transitions.copy()

        # Inversion des états finaux
        tous_etats = set(range(self.num_etats))
        anciens_finaux = set(self.etats_finaux)
        auto_comp.etats_finaux = list(tous_etats - anciens_finaux)
        auto_comp.num_etats_finaux = len(auto_comp.etats_finaux)
        
        print("Automate complémentaire généré avec succès.")
        return auto_comp
    
    def est_minimal(self):
        """Vérifie si l'automate a été marqué comme réduit par l'algorithme de Moore."""
        return hasattr(self, 'is_minimized') and self.is_minimized

    def minimiser(self):
        # 1. Moore ne s'applique que sur un automate déterministe et complet
        if not self.est_deterministe() or not self.est_complet():
            print("L'automate doit être DÉTERMINISTE et COMPLET pour être minimisé.")
            return self

        # On définit l'alphabet de travail en excluant explicitement epsilon (£)
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        alphabet = [sym for sym in alphabet if sym != "£"]
        
        # 2. Partition initiale : Terminaux (T) et Non-Terminaux (NT)
        etats_T = set(self.etats_finaux)
        etats_NT = set(range(self.num_etats)) - etats_T
        
        partitions_info = []
        if etats_NT: partitions_info.append({'type': 'NT', 'etats': etats_NT})
        if etats_T: partitions_info.append({'type': 'T', 'etats': etats_T})

        numero_etape = 0
        
        def afficher_P(n, info):
            affichage = []
            c_t_local, c_nt_local = 1, 1
            for group in info:
                label = f"{group['type']}{c_t_local if group['type']=='T' else c_nt_local}"
                if group['type'] == 'T': c_t_local += 1
                else: c_nt_local += 1
                affichage.append(f"{label}:{sorted(list(group['etats']))}")
            print(f"P{n} = [{', '.join(affichage)}]")

        print("\n--- Phase de Minimisation (Algorithme de Moore) ---")
        afficher_P(numero_etape, partitions_info)

        # 3. BOUCLE DE MOORE
        while True:
            nouvelles_partitions_info = []
            print(f"\nAnalyse des transitions pour P{numero_etape} :")
            
            for group in partitions_info:
                subgroups = {}
                for etat in group['etats']:
                    comportement = []
                    labels_trans = []
                    for s in alphabet:
                        # On prend le premier état d'arrivée (car déterministe)
                        dest_list = self.transitions.get((etat, s), [])
                        dest = dest_list[0] if dest_list else -1
                        
                        # Trouver le label du groupe de destination
                        dest_label = "???"
                        tmp_t, tmp_nt = 1, 1
                        for g_info in partitions_info:
                            this_label = f"{g_info['type']}{tmp_t if g_info['type']=='T' else tmp_nt}"
                            if g_info['type'] == 'T': tmp_t += 1
                            else: tmp_nt += 1
                            if dest in g_info['etats']:
                                dest_label = this_label
                                break
                        
                        comportement.append(dest_label)
                        labels_trans.append(f"({s}->{dest_label})")
                    
                    print(f"  État {etat} : {' '.join(labels_trans)}")
                    key = tuple(comportement)
                    if key not in subgroups: subgroups[key] = set()
                    subgroups[key].add(etat)
                
                # On conserve le type (T ou NT) du groupe parent
                for sub in subgroups.values():
                    nouvelles_partitions_info.append({'type': group['type'], 'etats': sub})
            
            # Si le nombre de groupes n'a pas changé, on a fini
            if len(nouvelles_partitions_info) == len(partitions_info):
                break
            
            partitions_info = nouvelles_partitions_info
            numero_etape += 1
            afficher_P(numero_etape, partitions_info)

        # 4. RECONSTRUCTION
        if len(partitions_info) == self.num_etats:
            print("\nL'automate est déjà minimal.")
            self.is_minimized = True
            return self

        auto_min = Automate()
        auto_min.num_symboles = self.num_symboles
        auto_min.num_etats = len(partitions_info)
        
        correspondance = {}
        c_t, c_nt = 1, 1
        print("\nTable de correspondance (AFDC -> AFDCM) :")
        for i, group in enumerate(partitions_info):
            label = f"{group['type']}{c_t if group['type']=='T' else c_nt}"
            if group['type'] == 'T': c_t += 1
            else: c_nt += 1
            
            print(f"  Nouvel état {i} ({label}) <-- regroupe : {sorted(list(group['etats']))}")
            for etat in group['etats']:
                correspondance[etat] = i

        # Paramètres de l'automate minimal
        auto_min.etats_initiaux = list(set(correspondance[e] for e in self.etats_initiaux))
        auto_min.num_etats_initiaux = len(auto_min.etats_initiaux)
        auto_min.etats_finaux = list(set(correspondance[e] for e in self.etats_finaux))
        auto_min.num_etats_finaux = len(auto_min.etats_finaux)

        # Reconstruction des transitions
        for i, group in enumerate(partitions_info):
            rep = list(group['etats'])[0]
            for s in alphabet:
                if (rep, s) in self.transitions:
                    dest_origine = self.transitions[(rep, s)][0]
                    auto_min.transitions[(i, s)] = [correspondance[dest_origine]]

        auto_min.is_minimized = True
        print(f"Minimisation terminée : {auto_min.num_etats} états restants.")
        return auto_min
    
    def reconnaitre_mot(self, mot):
        """Parcours l'automate pour vérifier si le mot est accepté."""
        # On commence par la fermeture-epsilon des états initiaux
        etats_actuels = set(self.fermeture_epsilon(self.etats_initiaux))
        
        # Cas du mot vide (noté £ dans les tests, mais "" en Python)
        if mot == "" or mot == "£":
            return any(e in self.etats_finaux for e in etats_actuels)

        for symbole in mot:
            prochains_etats = set()
            for etat in etats_actuels:
                if (etat, symbole) in self.transitions:
                    # On ajoute les destinations + leur fermeture epsilon
                    destinations = self.transitions[(etat, symbole)]
                    prochains_etats.update(self.fermeture_epsilon(destinations))
            
            etats_actuels = prochains_etats
            if not etats_actuels: # Si on est bloqué, le mot est refusé
                return False

        # Le mot est accepté si un des états atteints est final
        return any(e in self.etats_finaux for e in etats_actuels)
    
    def automate_epsilon(self):
        return any(sym == "£" for (_, sym) in self.transitions.keys())
    
    
    def fermeture_epsilon(self, etats):
        """Calcule l'ensemble des états accessibles via des transitions £."""
        fermeture = set(etats)
        pile = list(etats)
        while pile:
            u = pile.pop()
            if (u, "£") in self.transitions:
                for v in self.transitions[(u, "£")]:
                    if v not in fermeture:
                        fermeture.add(v)
                        pile.append(v)
        return frozenset(fermeture)

    if __name__ == "__main__":
        try:
            from main import menu_principal
            menu_principal()
        except ImportError:
            print("Erreur : Assurez-vous que main.py est dans le même dossier.")
