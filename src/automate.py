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
            print(f"✅ Fichier '{chemin_fichier}' chargé.")
        except Exception as e:
            print(f"❌ Erreur lecture : {e}")

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
        symboles_presents = set(sym for (_, sym) in self.transitions.keys())
        alphabet = sorted(list(symboles_presents)) if symboles_presents else [" "]
        
        lignes = []
        for etat in range(self.num_etats):
            marq = ""
            if etat in self.etats_initiaux: marq += "E "
            if etat in self.etats_finaux: marq += "S"
            
            dests = []
            for sym in alphabet:
                target = self.transitions.get((etat, sym), [])
                dests.append(",".join(str(d) for d in target) if target else "--")
            lignes.append((marq.strip(), str(etat), dests))

        largeurs = [max(len(sym), max([len(l[2][i]) for l in lignes] + [0])) for i, sym in enumerate(alphabet)]

        print("\n======== TABLEAU DE TRANSITION =========")
        head = f"{'':<5} | "
        for i, sym in enumerate(alphabet):
            head += f"{sym:<{largeurs[i]}} | "
        print(head + "\n" + "-"*len(head))

        for m, e, cols in lignes:
            ligne_str = f"{m:<3} {e:<1} | "
            for i, d in enumerate(cols):
                ligne_str += f"{d:<{largeurs[i]}} | "
            print(ligne_str)
        print("========================================\n")

    def est_standard(self):
        if self.num_etats_initiaux != 1: return False
        init = self.etats_initiaux[0]
        return not any(init in dests for dests in self.transitions.values())

    def standardiser(self):
        if self.est_standard(): return self
        new_init = self.num_etats
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        new_finaux = list(self.etats_finaux)
        
        if any(e in self.etats_finaux for e in self.etats_initiaux):
            new_finaux.append(new_init)

        new_trans = self.transitions.copy()
        for sym in alphabet:
            targets = set()
            for e_old in self.etats_initiaux:
                targets.update(self.transitions.get((e_old, sym), []))
            if targets: new_trans[(new_init, sym)] = list(targets)

        self.num_etats += 1
        self.etats_initiaux = [new_init]
        self.num_etats_initiaux = 1
        self.etats_finaux = new_finaux
        self.transitions = new_trans
        return self

    def determiniser(self):
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
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        for i in range(self.num_etats):
            for sym in alphabet:
                if (i, sym) not in self.transitions: return False
        return True

    def completer(self):
        if self.est_complet(): return
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        poubelle = self.num_etats
        self.num_etats += 1
        for i in range(self.num_etats):
            for sym in alphabet:
                if (i, sym) not in self.transitions:
                    self.transitions[(i, sym)] = [poubelle]
        print(f"État poubelle {poubelle} ajouté.")

    def minimiser(self):
        if not self.est_deterministe(): self = self.determiniser()
        if not self.est_complet(): self.completer()
        
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        finaux = set(self.etats_finaux)
        non_finaux = set(range(self.num_etats)) - finaux
        
        P = [non_finaux, finaux] if non_finaux else [finaux]
        
        while True:
            new_P = []
            for groupe in P:
                subgroups = {}
                for etat in groupe:
                    key = []
                    for sym in alphabet:
                        dest = self.transitions[(etat, sym)][0]
                        idx = next((i for i, g in enumerate(P) if dest in g), -1)
                        key.append(idx)
                    k = tuple(key)
                    if k not in subgroups: subgroups[k] = set()
                    subgroups[k].add(etat)
                new_P.extend(subgroups.values())
            
            if len(new_P) == len(P): break
            P = new_P

        auto_min = Automate()
        auto_min.num_symboles = self.num_symboles
        auto_min.num_etats = len(P)
        mapping = {e: i for i, g in enumerate(P) for e in g}
        
        auto_min.etats_initiaux = list(set(mapping[e] for e in self.etats_initiaux))
        auto_min.etats_finaux = list(set(mapping[e] for e in self.etats_finaux))
        
        for i, g in enumerate(P):
            rep = list(g)[0]
            for sym in alphabet:
                dest = self.transitions[(rep, sym)][0]
                auto_min.transitions[(i, sym)] = [mapping[dest]]
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