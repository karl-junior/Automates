# Creation de la classe Automate
class Automate:

    #definition de la fonction de lecture
    def read_txt(self,file):
        with open(file, "r") as file :
            automate = file.readlines()
            self.num_symbols = int(automate[0].strip()) # initialisation du nombre de symbole
            self.num_states = int(automate[1].strip()) # initialisation du nombre d'etats

            initial_line = automate[2].strip().split()
            self.num_initial_states = int(initial_line[0]) #initialisation du
            self.initial_states = list(map(int,initial_line[1:]))

            final_line = automate[3].strip().split()
            self.num_final_states = final_line[0]
            self.final_states = list(map(int,final_line[1:]))


            self.num_transitions = int(automate[4].strip())
            self.transitions = {}
            if self.num_transitions != 0 :
                for i in range(5, 5 + self.num_transitions):
                    line = automate[i].strip()

                    j= 0
                    while line[j].isdigit() :
                        j += 1

                    debut = int(line[:j])
                    altphabet = line[j]
                    fin = int(line[j+1:])

                    key = (debut, altphabet)
                    if key not in self.transitions.keys():
                        self.transitions[key] = []

                    self.transitions[key].append(fin)

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
    
    def is_deterministic():
        return

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

    

    
    
