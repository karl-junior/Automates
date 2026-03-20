# Creation de la classe Automate
class Automate:

    # definition de la fonction de lecture
    def read_txt(self,file):
        try : 
            with open(file, "r") as file :
                automate = file.readlines()

                # initialisation du nombre de symbole de l'alphabet
                self.num_symbols = int(automate[0].strip())

                # initialisation du nombre d'etats
                self.num_states = int(automate[1].strip()) 

                # etat initiaux
                initial_line = automate[2].strip().split()
                self.num_initial_states = int(initial_line[0]) # nombre d'etats initiaux
                self.initial_states = list(map(int,initial_line[1:])) # liste des etats initiaux

                # etat finaux
                final_line = automate[3].strip().split() 
                self.num_final_states = int(final_line[0]) # nombre d'etats finaux
                self.final_states = list(map(int,final_line[1:]))# liste des etats finaux

                # initialisation du numbre de transition
                self.num_transitions = int(automate[4].strip())

                # transitions (c'est une bibliothéque)
                # clé = (état de depart, symbole) = liste d'etats d'arrivée
                self.transitions = {}

                if self.num_transitions != 0 :
                    for i in range(5, 5 + self.num_transitions):
                        line = automate[i].strip()

                        # on cherche où s'arrête l'etat de depart
                        j= 0
                    while line[j].isdigit() :
                        j += 1
                    
                    # extration de l'etat de depart
                    debut = int(line[:j])

                    # extraction du symbole de transition
                    altphabet = line[j]

                    # extraction de l'etat d'arrivée
                    fin = int(line[j+1:])

                    # creation de la clé (etat de depart, symbole)
                    key = (debut, altphabet)

                    # si la clé n'existe pas, on initialse
                    if key not in self.transitions.keys():
                        self.transitions[key] = []
                    
                    # ajout de l'etat d'arrivée à la lite des transitions
                    self.transitions[key].append(fin)
        except FileNotFoundError :
            print("le fichier n'existe pas")



    def display():
        return

    def standardize():
        return

    def is_standardized():
        return
    
    def determinize():
        start_state = frozenset(self.initial_states)

        new_states = [start_state]
        new_transitions = {}
        new_final_states = []



        return

    def is_deterministic(self):
        # verification du nombre d'etats initial
        if(self.num_initial_states > 1):
            return False
        
        # Verification d'une unique transition pour chaque couple (etat, symbole)
        for key in self.transitions:
            if len(self.transitions[key]) > 1 :
                return False
        return True
    

    def complete():
        return

    def is_complete():
        return

    def minimize():
        return

    def is_minimized():
        return

    def recognize_words():
        return
    
    def complementary_language():
        return

    

    
    
