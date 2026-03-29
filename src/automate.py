# Creation de la classe Automate
class Automate:

    # definition de la fonction de lecture
    def lire_fichier(self, chemin_fichier):
        try:
            with open(chemin_fichier, "r") as fichier:
                automate = fichier.readlines()

                # initialisation du nombre de symboles de l'alphabet
                self.num_symboles = int(automate[0].strip())

                # initialisation du nombre d'etats
                self.num_etats = int(automate[1].strip())

                # etats initiaux
                ligne_initiale = automate[2].strip().split()
                self.num_etats_initiaux = int(ligne_initiale[0])
                self.etats_initiaux = [int(x) for x in ligne_initiale[1:]]

                # etats finaux
                ligne_finale = automate[3].strip().split()
                self.num_etats_finaux = int(ligne_finale[0])
                self.etats_finaux = [int(x) for x in ligne_finale[1:]]

                # initialisation du nombre de transitions
                self.num_transitions = int(automate[4].strip())

                # transitions
                # clé = (état de depart, symbole) = liste d'etats d'arrivée
                self.transitions = {}

                if self.num_transitions != 0:
                    for i in range(5, 5 + self.num_transitions):
                        ligne = automate[i].strip()

                        # on cherche où s'arrête l'etat de depart
                        j = 0
                        while j < len(ligne) and ligne[j].isdigit():
                            j += 1

                        # extraction de l'etat de depart
                        debut = int(ligne[:j])

                        # extraction du symbole de transition
                        symbole = ligne[j]

                        # extraction de l'etat d'arrivée
                        fin = int(ligne[j + 1:])

                        # creation de la clé (etat de depart, symbole)
                        cle = (debut, symbole)

                        # si la clé n'existe pas, on initialise
                        if cle not in self.transitions:
                            self.transitions[cle] = []

                        # ajout de l'etat d'arrivée à la liste des transitions
                        self.transitions[cle].append(fin)

        except FileNotFoundError:
            print(f"Erreur : le fichier '{chemin_fichier}' n'existe pas.")

    def afficher(self):
        # genere l'alphabet
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]

        # Préparation des données de chaque ligne
        lignes = []
        for etat in range(self.num_etats):
            # precise si c'est un etat entree ou sortie
            marqueur = ""
            if etat in self.etats_initiaux:
                marqueur += "E "
            if etat in self.etats_finaux:
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
        print(f"États initiaux : {self.etats_initiaux}")
        print(f"États terminaux : {self.etats_finaux}\n")

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

    # Un automate est standard si :
    # Il a 1 etat initial
    # Aucune transition ne revient vers l'état initial
    def est_standard(self):
        if self.num_etats_initiaux != 1:
            return False
        
        etat_initial = self.etats_initiaux[0]
        
        # On parcourt toutes les listes de destinations dans le dictionnaire
        for destinations in self.transitions.values():
            if etat_initial in destinations:
                return False
                
        return True

    def standardiser(self):
        if self.est_standard():
            print("L'automate est déjà standard.")
            return self

        # On crée un nouvel indice pour l'état standard (le dernier + 1)
        nouvel_initial = self.num_etats
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        
        # Les futurs états finaux sont les mêmes que les anciens
        nouveaux_finaux = list(self.etats_finaux)
        
        # Si un ancien état initial était final -> le nouveau le devient aussi
        # Gestion du mot vide
        for e_init in self.etats_initiaux:
            if e_init in self.etats_finaux:
                if nouvel_initial not in nouveaux_finaux:
                    nouveaux_finaux.append(nouvel_initial)
                break

        # On copie les transitions actuelles
        nouvelles_transitions = self.transitions.copy()
        
        # Le nouvel état initial doit avoir les mêmes sorties que tous les anciens initiaux
        for symbole in alphabet:
            targets = set()
            for e_init in self.etats_initiaux:
                if (e_init, symbole) in self.transitions:
                    for t in self.transitions[(e_init, symbole)]:
                        targets.add(t)
            
            if targets:
                nouvelles_transitions[(nouvel_initial, symbole)] = list(targets)

        # On met à jour l'objet ou on en retourne un nouveau
        self.num_etats += 1
        self.etats_initiaux = [nouvel_initial]
        self.num_etats_initiaux = 1
        self.etats_finaux = nouveaux_finaux
        self.num_etats_finaux = len(nouveaux_finaux)
        self.transitions = nouvelles_transitions
        
        print(f"Automate standardisé. Nouvel état initial : {nouvel_initial}")
        return self

    def determiniser(self):
        # 1. L'état initial du nouvel automate est l'ensemble de tous les états initiaux
        etat_depart = frozenset(self.etats_initiaux)
        if not etat_depart:  # Cas particulier automate vide
            return Automate()

        nouveaux_etats = [etat_depart]
        nouvelles_transitions = {}
        nouveaux_etats_finaux = []
        file = [etat_depart]
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]

        while file:
            ensemble_courant = file.pop(0)

            # Si l'un des états d'origine est final, le nouvel état composé est final
            if any(s in self.etats_finaux for s in ensemble_courant):
                if ensemble_courant not in nouveaux_etats_finaux:
                    nouveaux_etats_finaux.append(ensemble_courant)

            for symbole in alphabet:
                ensemble_suivant = set()
                for etat in ensemble_courant:
                    # On utilise le dictionnaire self.transitions tel que défini dans lire_fichier
                    if (etat, symbole) in self.transitions:
                        for cible in self.transitions[(etat, symbole)]:
                            ensemble_suivant.add(cible)

                if ensemble_suivant:
                    cible_frozenset = frozenset(ensemble_suivant)
                    nouvelles_transitions[(ensemble_courant, symbole)] = cible_frozenset

                    if cible_frozenset not in nouveaux_etats:
                        nouveaux_etats.append(cible_frozenset)
                        file.append(cible_frozenset)

        # 2. Construction du nouvel objet Automate
        auto_det = Automate()
        auto_det.num_symboles = self.num_symboles
        auto_det.num_etats = len(nouveaux_etats)

        # Mapping pour transformer les frozensets en numéros d'états (0, 1, 2...)
        correspondance = {etat: i for i, etat in enumerate(nouveaux_etats)}

        auto_det.etats_initiaux = [correspondance[etat_depart]]
        auto_det.num_etats_initiaux = 1
        auto_det.etats_finaux = [correspondance[s] for s in nouveaux_etats_finaux]
        auto_det.num_etats_finaux = len(auto_det.etats_finaux)

        # Reconstruction du dictionnaire de transitions
        auto_det.transitions = {}
        for (ens_source, sym), ens_dest in nouvelles_transitions.items():
            auto_det.transitions[(correspondance[ens_source], sym)] = [correspondance[ens_dest]]

        auto_det.num_transitions = len(auto_det.transitions)
        return auto_det

    def est_deterministe(self):
        # verification du nombre d'etats initial
        if (self.num_etats_initiaux > 1):
            return False

        # Verification d'une unique transition pour chaque couple (etat, symbole)
        for cle in self.transitions:
            if len(self.transitions[cle]) > 1:
                return False
        return True

    def completer(self):

        if self.est_complet():
            print("l'automate est déja complet")
            return
        if self.automate_epsilon():
            print("l'automate ne peut pas être completé")
            return

        # Generation de l'alphabet
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        nouvel_etat = self.num_etats
        self.num_etats += 1


        # si le couple (i,j) n'existe pas
        for i in range(nouvel_etat):
            for j in alphabet:
                if (i, j) not in self.transitions:
                    self.transitions[(i, j)] = [nouvel_etat]

        for j in alphabet:
            self.transitions[(nouvel_etat, j)] = [nouvel_etat]

        print(f"l'etat {nouvel_etat} represente l'etat final")

    def est_complet(self):
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]
        for i in range(self.num_etats):
            for j in alphabet:
                if (i, j) not in self.transitions:
                    return False
        return True

    def minimiser(self, test_auto_min=False):
        alphabet = [chr(ord('a') + i) for i in range(self.num_symboles)]

        etats_terminaux = set(self.etats_finaux)
        tous_les_etats = set(range(self.num_etats))
        etats_non_terminaux = tous_les_etats - etats_terminaux

        partitions = []
        if len(etats_non_terminaux) > 0:
            partitions.append(etats_non_terminaux)
        if len(etats_terminaux) > 0:
            partitions.append(etats_terminaux)

        numero_etape = 0
        if not test_auto_min:
            print(f"P{numero_etape} = {partitions}")

        partition_a_change = True

        while partition_a_change:
            nouvelles_partitions = []
            partition_a_change = False

            for groupe in partitions:
                # On classe les états de ce groupe selon leur comportement
                groupes_separes = {}

                for etat in groupe:

                    comportement = []  # Le comportement est la liste des groupes de destination pour chaque lettre

                    for symbole in alphabet:
                        if (etat, symbole) in self.transitions and len(self.transitions[(etat, symbole)]) > 0:
                            etat_arrivee = self.transitions[(etat, symbole)][0]

                            index_du_groupe_arrivee = -1
                            for index, p in enumerate(partitions):
                                if etat_arrivee in p:
                                    index_du_groupe_arrivee = index
                                    break

                            comportement.append(index_du_groupe_arrivee)
                        else:
                            # S'il manque une transition (même si ça ne devrait pas arriver sur un automate complet)
                            comportement.append(-1)

                    # On regroupe les états qui ont exactement le même comportement
                    comportement = tuple(comportement)
                    if comportement not in groupes_separes:
                        groupes_separes[comportement] = set()
                    groupes_separes[comportement].add(etat)

                # Si on a créé plus d'un sous-groupe, c'est qu'on a dû diviser notre groupe de départ
                if len(groupes_separes) > 1:
                    partition_a_change = True

                # On ajoute tous les groupes à la liste du prochain tour
                for sous_groupe in groupes_separes.values():
                    nouvelles_partitions.append(sous_groupe)

            # Mise à jour pour le tour de boucle suivant
            if partition_a_change:
                partitions = nouvelles_partitions
                numero_etape += 1
                if not test_auto_min:
                    print(f"P{numero_etape} = {partitions}")


        if test_auto_min: # teste la minimalité
            return len(partitions) == self.num_etats

        # Creation de l'automate :
        print("-" * 30)
        if numero_etape == 0:
            print("L'automate d'origine est déjà minimal !")
            return self

        print(f"Automate minimal trouvé en {numero_etape} étapes.")

        auto_min = Automate()
        auto_min.num_symboles = self.num_symboles
        auto_min.num_etats = len(partitions)

        # On crée un annuaire pour savoir quel ancien état devient quel nouveau numéro
        correspondance = {}
        for indice_nouveau_etat, groupe in enumerate(partitions):
            for ancien_etat in groupe:
                correspondance[ancien_etat] = indice_nouveau_etat

        # Nouveaux états initiaux
        nouveaux_initiaux = set()
        for etat in self.etats_initiaux:
            nouveau_numero = correspondance[etat]
            nouveaux_initiaux.add(nouveau_numero)
        auto_min.etats_initiaux = list(nouveaux_initiaux)
        auto_min.num_etats_initiaux = len(auto_min.etats_initiaux)

        # Nouveaux états finaux
        nouveaux_finaux = set()
        for etat in self.etats_finaux:
            nouveau_numero = correspondance[etat]
            nouveaux_finaux.add(nouveau_numero)
        auto_min.etats_finaux = list(nouveaux_finaux)
        auto_min.num_etats_finaux = len(auto_min.etats_finaux)

        # Nouvelles transitions
        auto_min.transitions = {}
        for indice_nouveau_etat, groupe in enumerate(partitions):
            # Tous les états du groupe ont le même comportement, on en prend un au hasard
            etat_representant = list(groupe)[0]

            for symbole in alphabet:
                if (etat_representant, symbole) in self.transitions and len(
                        self.transitions[(etat_representant, symbole)]) > 0:
                    ancien_arrivee = self.transitions[(etat_representant, symbole)][0]
                    nouveau_arrivee = correspondance[ancien_arrivee]

                    auto_min.transitions[(indice_nouveau_etat, symbole)] = [nouveau_arrivee]

        auto_min.num_transitions = len(auto_min.transitions)
        return auto_min

    def est_minimal(self):
        # Un automate doit être déterministe et complet pour que ce test soit valable
        if not self.est_deterministe() or not self.est_complet():
            return False

        # On délègue le travail à la fonction minimiser en mode silencieux
        return self.minimiser(test_auto_min=True)

    def reconnaitre_mot(self, mot):
        # Au départ, on initialise les états actifs avec le ou les états initiaux de l'automate
        etats_courants = set(self.etats_initiaux)

        # On parcourt le mot séquence par séquence (lettre par lettre)
        # On ne mémorise pas la chaîne entière, on avance d'une étape à chaque caractère lu
        for lettre in mot:

            # À chaque nouvelle lettre, on crée un ensemble vide
            # On réinitialise la mémoire temporaire pour ne stocker que les destinations de cette étape précise
            prochains_etats = set()

            # On examine chaque état dans lequel on se trouve à cet instant précis
            for etat in etats_courants:

                # On vérifie si la fonction de transition définit un chemin pour cette lettre depuis cet état
                if (etat, lettre) in self.transitions:

                    # Si la transition existe, on parcourt tous les états d'arrivée possibles
                    for etat_arrivee in self.transitions[(etat, lettre)]:
                        # On ajoute ces états cibles dans l'ensemble temporaire
                        # L'utilisation d'un ensemble (set) garantit qu'on ne stocke pas de doublons
                        prochains_etats.add(etat_arrivee)

            # La lecture de la lettre est terminée : on remplace les états précédents par ces nouveaux états atteints
            etats_courants = prochains_etats

            # Si l'ensemble des états courants est vide, c'est qu'aucune transition n'était possible
            # On se trouve dans un cul-de-sac
            if len(etats_courants) == 0:
                return False  # On rejette le mot immédiatement

        # La lecture complète du mot est terminée. On examine l'ensemble des états atteints
        for etat in etats_courants:
            # Si au moins un de ces états est un état terminal
            if etat in self.etats_finaux:
                return True  # Le mot est officiellement reconnu par l'automate

        # Si l'on a terminé la lecture mais qu'on ne se trouve sur aucun état terminal
        return False  # Le mot n'appartient pas au langage, on le rejette

    # Transformation de l'automate en son automate complémentaire
    def automate_complementaire(self):
        nouveaux_etats_finaux = []
        for etat in range(self.num_etats):
            if etat not in self.etats_finaux:
                nouveaux_etats_finaux.append(etat)
        self.etats_finaux = nouveaux_etats_finaux
        self.num_etats_finaux = len(nouveaux_etats_finaux)
        print("Automate est transformé en son complémentaire.")

    def automate_epsilon(self):
        for (i, j) in self.transitions:
            if j == "£":
                return True
        return False
