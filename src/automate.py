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

    def est_deterministe(self):
        # AJOUT PRINT EXPLICATIONS
        if self.num_etats_initiaux > 1:
            print(f"   -> Non-déterministe : {self.num_etats_initiaux} états initiaux trouvés (il en faut 1).")
            return False
        if self.automate_epsilon():
            print("   -> Non-déterministe : présence de transitions epsilon (£).")
            return False
        
        for (etat, sym), destinations in self.transitions.items():
            if len(destinations) > 1:
                print(f"   -> Non-déterministe : l'état {etat} possède plusieurs sorties pour '{sym}' vers {destinations}.")
                return False
        return True

    def determiniser(self):
        if self.est_deterministe():
            print("L'automate est déjà DÉTERMINISTE. Opération annulée.")
            return self
        
        # AJOUT PRINT EXPLICATIONS
        print("   [Action] Début de la déterminisation (algorithme par sous-ensembles)...")
        
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
                        # EXPLICATION DES ÉTATS COMPOSÉS
                        print(f"      * Nouvel état composé créé : {list(next_set)}")
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

    def est_complet(self):
        alphabet_reel = set(sym for (_, sym) in self.transitions.keys() if sym != "£")
        if not alphabet_reel: return True

        for i in range(self.num_etats):
            for sym in alphabet_reel:
                if (i, sym) not in self.transitions or not self.transitions[(i, sym)]:
                    # AJOUT PRINT EXPLICATIONS
                    print(f"   -> Non-complet : l'état {i} n'a pas de transition pour le symbole '{sym}'.")
                    return False
        return True

    def completer(self):
        if self.est_complet():
            print("L'automate est déjà complet.")
            return
    
        alphabet_reel = sorted(list(set(sym for (_, sym) in self.transitions.keys() if sym != "£")))
        poubelle = self.num_etats
        poubelle_creee = False

        for i in range(self.num_etats):
            for sym in alphabet_reel:
                if (i, sym) not in self.transitions or not self.transitions[(i, sym)]:
                    if not poubelle_creee:
                        # AJOUT PRINT EXPLICATIONS
                        print(f"   [Action] Création d'un état poubelle (état {poubelle}) pour compléter l'automate.")
                        self.num_etats += 1
                        poubelle_creee = True
                    self.transitions[(i, sym)] = [poubelle]

        if poubelle_creee:
            for sym in alphabet_reel:
                self.transitions[(poubelle, sym)] = [poubelle]
            print(f"   -> Résultat : État poubelle {poubelle} ajouté et bouclé sur l'alphabet.")

    def est_standard(self):
        if self.num_etats_initiaux != 1: 
            # AJOUT PRINT EXPLICATIONS
            print(f"   -> Non-standard : il y a {self.num_etats_initiaux} états initiaux (il en faut 1 seul).")
            return False
        init = self.etats_initiaux[0]
        for (etat, sym), dests in self.transitions.items():
            if init in dests:
                # AJOUT PRINT EXPLICATIONS
                print(f"   -> Non-standard : l'état {etat} possède une transition '{sym}' vers l'état initial {init}.")
                return False
        return True

    def standardiser(self):
        if self.est_standard():
            print("L'automate est déjà STANDARD. Opération annulée.")
            return self
        
        # AJOUT PRINT EXPLICATIONS
        print(f"   [Action] Création d'un nouvel état initial {self.num_etats} déconnecté de toute transition entrante.")

        new_init = self.num_etats
        alphabet_complet = set(sym for (_, sym) in self.transitions.keys())
        new_trans = self.transitions.copy()
        new_finaux = list(self.etats_finaux)

        for sym in alphabet_complet:
            targets = set()
            for e_old in self.etats_initiaux:
                if (e_old, sym) in self.transitions:
                    targets.update(self.transitions[(e_old, sym)])
            
            if targets:
                new_trans[(new_init, sym)] = list(targets)

        if any(e in self.etats_finaux for e in self.etats_initiaux):
            if new_init not in new_finaux:
                new_finaux.append(new_init)

        self.num_etats += 1
        self.etats_initiaux = [new_init]
        self.num_etats_initiaux = 1
        self.etats_finaux = new_finaux
        self.transitions = new_trans
        return self

    def est_minimal(self):
        # Ajout d'une vérification silencieuse pour le complémentaire
        if not self.est_deterministe() or not self.est_complet():
            return False
        # Logique simplifiée : si Moore ne peut plus diviser, c'est minimal
        # (Cette fonction peut être appelée par complementaire)
        return True

    def complementaire(self):
        if not self.est_deterministe() or not self.est_complet():
            print("Erreur : L'automate doit être DÉTERMINISTE et COMPLET.")
            return None

        print(f"\n   [Action] Construction du complémentaire par inversion des états finaux.")

        auto_comp = Automate()
        auto_comp.num_symboles = self.num_symboles
        auto_comp.num_etats = self.num_etats
        auto_comp.etats_initiaux = list(self.etats_initiaux)
        auto_comp.num_etats_initiaux = self.num_etats_initiaux
        auto_comp.transitions = self.transitions.copy()

        nouveaux_finaux = [i for i in range(self.num_etats) if i not in self.etats_finaux]
        auto_comp.etats_finaux = nouveaux_finaux
        auto_comp.num_etats_finaux = len(nouveaux_finaux)
        
        return auto_comp

    def minimiser(self):
        if not self.est_deterministe() or not self.est_complet():
            print("⚠️ L'automate doit être DÉTERMINISTE et COMPLET pour être minimisé.")
            return self

        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        alphabet = [sym for sym in alphabet if sym != "£"]
        
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

        afficher_P(numero_etape, partitions_info)

        while True:
            nouvelles_partitions_info = []
            print(f"\nAnalyse des transitions pour P{numero_etape} :")
            
            for group in partitions_info:
                subgroups = {}
                for etat in group['etats']:
                    comportement = []
                    labels_trans = []
                    for s in alphabet:
                        dest_list = self.transitions.get((etat, s), [])
                        dest = dest_list[0] if dest_list else -1
                        
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
                
                for sub in subgroups.values():
                    nouvelles_partitions_info.append({'type': group['type'], 'etats': sub})
            
            if len(nouvelles_partitions_info) == len(partitions_info):
                break
            
            partitions_info = nouvelles_partitions_info
            numero_etape += 1
            afficher_P(numero_etape, partitions_info)

        if len(partitions_info) == self.num_etats:
            print("\n✅ L'automate est déjà minimal.")
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
            
            print(f"  Nouvel état {i} ({label}) <-- {sorted(list(group['etats']))}")
            for etat in group['etats']:
                correspondance[etat] = i

        auto_min.etats_initiaux = list(set(correspondance[e] for e in self.etats_initiaux))
        auto_min.num_etats_initiaux = len(auto_min.etats_initiaux)
        auto_min.etats_finaux = list(set(correspondance[e] for e in self.etats_finaux))
        auto_min.num_etats_finaux = len(auto_min.etats_finaux)

        for i, group in enumerate(partitions_info):
            rep = list(group['etats'])[0]
            for s in alphabet:
                if (rep, s) in self.transitions:
                    auto_min.transitions[(i, s)] = [correspondance[self.transitions[(rep, s)][0]]]

        return auto_min
    
    def reconnaitre_mot(self, mot):
        currents = self.fermeture_epsilon(self.etats_initiaux)
        for char in mot:
            next_step = set()
            for e in currents:
                next_step.update(self.transitions.get((e, char), []))
            currents = self.fermeture_epsilon(next_step)
            if not currents: 
                return False
        
        return any(e in self.etats_finaux for e in currents)
    
    def automate_epsilon(self):
        return any(sym == "£" for (_, sym) in self.transitions.keys())
    
    def fermeture_epsilon(self, etats):
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
#fin 
