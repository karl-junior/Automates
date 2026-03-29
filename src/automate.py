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
            # Gestion flexible du chemin (racine ou dossier tests)
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
                        if (deb, sym) not in self.transitions:
                            self.transitions[(deb, sym)] = []
                        if fin not in self.transitions[(deb, sym)]:
                            self.transitions[(deb, sym)].append(fin)
            print(f"Fichier '{chemin_fichier}' chargé.")
        except Exception as e:
            print(f"Erreur lecture : {e}")

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

    def afficher(self):
        # 1. Préparation de l'alphabet (on ignore le £ pour le tri, on l'ajoute à la fin)
        symboles_presents = set(sym for (_, sym) in self.transitions.keys())
        alphabet = sorted([s for s in symboles_presents if s != "£"])
        if "£" in symboles_presents:
            alphabet.append("£")
        
        if not alphabet: alphabet = [" "]

        # 2. Préparation des données et calcul de la largeur max pour les destinations
        lignes = []
        largeurs_colonnes = [len(sym) for sym in alphabet]

        for etat in range(self.num_etats):
            marqueur = ""
            if etat in self.etats_initiaux: marqueur += "E "
            if etat in self.etats_finaux: marqueur += "S"
            
            destinations = []
            for i, symbole in enumerate(alphabet):
                cle = (etat, symbole)
                if cle in self.transitions:
                    dests_str = ",".join(str(d) for d in sorted(self.transitions[cle]))
                else:
                    dests_str = "--"
                
                destinations.append(dests_str)
                # Mise à jour de la largeur de la colonne si le contenu est plus large
                if len(dests_str) > largeurs_colonnes[i]:
                    largeurs_colonnes[i] = len(dests_str)
            
            lignes.append((marqueur.strip(), str(etat), destinations))

        # 3. Calcul de la largeur de la colonne "État" (Marqueur + Numéro)
        # On cherche le plus long numéro d'état (ex: "12") + place pour "E S "
        largeur_etat = max(len(l[1]) for l in lignes) if lignes else 1
        largeur_col_gauche = 4 + largeur_etat # 4 espaces pour "E S "

        # 4. Affichage du tableau
        print("\n" + "="*20 + " TABLEAU DE TRANSITION " + "="*20)
        
        # En-tête
        en_tete = f"{'':<{largeur_col_gauche}} | "
        for i, symbole in enumerate(alphabet):
            en_tete += f"{symbole:^{largeurs_colonnes[i]}} | " # Centré
        
        print(en_tete)
        print("-" * len(en_tete))

        # Contenu
        for marqueur, num_etat, cols in lignes:
            # On aligne le marqueur à gauche et le numéro d'état juste après
            # Exemple: "E S  12  | "
            label_etat = f"{marqueur:<3} {num_etat:>{largeur_etat}}"
            ligne_str = f"{label_etat} | "
            
            for i, dest in enumerate(cols):
                ligne_str += f"{dest:<{largeurs_colonnes[i]}} | "
            
            print(ligne_str)
        
        print("=" * len(en_tete) + "\n")

    def est_standard(self):
        if self.num_etats_initiaux != 1: return False
        init = self.etats_initiaux[0]
        return not any(init in dests for dests in self.transitions.values())

    def standardiser(self):
        if self.est_standard():
            print("L'automate est déjà STANDARD. Opération annulée.")
            return self
        
        # 1. Créer le nouvel état initial (index = num_etats actuel)
        new_init = self.num_etats
        
        # 2. Identifier TOUS les symboles (y compris £)
        alphabet_complet = set(sym for (_, sym) in self.transitions.keys())
        
        new_trans = self.transitions.copy()
        new_finaux = list(self.etats_finaux)

        # 3. Le nouvel état doit avoir les mêmes sorties que TOUS les anciens initiaux
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
            if new_init not in new_finaux:
                new_finaux.append(new_init)

        # 5. Mise à jour de l'objet
        self.num_etats += 1
        self.etats_initiaux = [new_init]
        self.num_etats_initiaux = 1
        self.etats_finaux = new_finaux
        self.transitions = new_trans
        
        return self

    def determiniser(self):
        if self.est_deterministe():
            print("L'automate est déjà DÉTERMINISTE. Opération annulée.")
            return self
        
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
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
        return auto_det

    def est_deterministe(self):
        if self.num_etats_initiaux > 1 or self.automate_epsilon(): return False
        return all(len(v) <= 1 for v in self.transitions.values())

    def est_complet(self):
        # On récupère l'alphabet réel (a, b...) en ignorant epsilon
        alphabet_reel = set(sym for (_, sym) in self.transitions.keys() if sym != "£")
        
        if not alphabet_reel:
            return True # Automate vide ou uniquement epsilon

        for i in range(self.num_etats):
            for sym in alphabet_reel:
                # Si un état n'a pas de transition pour une des lettres de l'alphabet
                if (i, sym) not in self.transitions or not self.transitions[(i, sym)]:
                    return False
        return True

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
            # La poubelle doit boucler sur toutes les lettres
            for sym in alphabet_reel:
                self.transitions[(poubelle, sym)] = [poubelle]
            print(f"État poubelle {poubelle} ajouté.")


    def complementaire(self):
        # Sécurité : le complémentaire nécessite un automate déterministe et complet
        if not self.est_deterministe() or not self.est_complet():
            print("Erreur : L'automate doit être DÉTERMINISTE et COMPLET pour calculer le complémentaire.")
            return None

        # On crée une copie de l'automate
        auto_comp = Automate()
        auto_comp.num_symboles = self.num_symboles
        auto_comp.num_etats = self.num_etats
        auto_comp.etats_initiaux = list(self.etats_initiaux)
        auto_comp.num_etats_initiaux = self.num_etats_initiaux
        auto_comp.transitions = self.transitions.copy()

        # INVERSION DES ÉTATS FINAUX
        # Tous les états qui n'étaient PAS finaux le deviennent
        nouveaux_finaux = []
        for i in range(self.num_etats):
            if i not in self.etats_finaux:
                nouveaux_finaux.append(i)
        
        auto_comp.etats_finaux = nouveaux_finaux
        auto_comp.num_etats_finaux = len(nouveaux_finaux)
        
        print("Automate complémentaire généré.")
        return auto_comp

    def minimiser(self, test_auto_min=False):
        if not test_auto_min and self.minimiser(test_auto_min=True):
            print("L'automate est déjà MINIMAL. Opération annulée.")
            return self
        # On définit l'alphabet réel en excluant epsilon et en se basant sur num_symboles
        # Si num_symboles est 2, on ne prend que 'a' et 'b'
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]

        etats_terminaux = set(self.etats_finaux)
        tous_les_etats = set(range(self.num_etats))
        etats_non_terminaux = tous_les_etats - etats_terminaux

        partitions = []
        if etats_non_terminaux: partitions.append(etats_non_terminaux)
        if etats_terminaux: partitions.append(etats_terminaux)

        while True:
            nouvelles_partitions = []
            for groupe in partitions:
                groupes_separes = {}
                for etat in groupe:
                    comportement = []
                    for symbole in alphabet:
                        # On vérifie si la transition existe pour éviter le KeyError
                        if (etat, symbole) in self.transitions and self.transitions[(etat, symbole)]:
                            etat_arrivee = self.transitions[(etat, symbole)][0]
                            # On trouve l'index du groupe de l'état d'arrivée
                            index_groupe = next((i for i, g in enumerate(partitions) if etat_arrivee in g), -1)
                            comportement.append(index_groupe)
                        else:
                            comportement.append(-1)
                    
                    c_tuple = tuple(comportement)
                    if c_tuple not in groupes_separes:
                        groupes_separes[c_tuple] = set()
                    groupes_separes[c_tuple].add(etat)
                
                nouvelles_partitions.extend(groupes_separes.values())

            if len(nouvelles_partitions) == len(partitions):
                break
            partitions = nouvelles_partitions

        if test_auto_min: return len(partitions) == self.num_etats

        # Reconstruction de l'automate minimal
        auto_min = Automate()
        auto_min.num_symboles = self.num_symboles
        auto_min.num_etats = len(partitions)
        
        correspondance = {etat: i for i, groupe in enumerate(partitions) for etat in groupe}

        auto_min.etats_initiaux = list(set(correspondance[e] for e in self.etats_initiaux))
        auto_min.num_etats_initiaux = len(auto_min.etats_initiaux)
        auto_min.etats_finaux = list(set(correspondance[e] for e in self.etats_finaux))
        auto_min.num_etats_finaux = len(auto_min.etats_finaux)

        for i, groupe in enumerate(partitions):
            representant = list(groupe)[0]
            for symbole in alphabet:
                if (representant, symbole) in self.transitions:
                    dest = self.transitions[(representant, symbole)][0]
                    auto_min.transitions[(i, symbole)] = [correspondance[dest]]
        
        return auto_min

    def reconnaitre_mot(self, mot):
        currents = self.fermeture_epsilon(self.etats_initiaux)
        for char in mot:
            next_step = set()
            for e in currents:
                next_step.update(self.transitions.get((e, char), []))
            currents = self.fermeture_epsilon(next_step)
            if not currents: return False
        return any(e in self.etats_finaux for e in currents)

    def automate_epsilon(self):
        return any(sym == "£" for (_, sym) in self.transitions.keys())
    

    if __name__ == "__main__":
        try:
            from main import menu_principal
            menu_principal()
        except ImportError:
            print("Erreur : Assurez-vous que main.py est dans le même dossier.")