import json
import sys
from collections import defaultdict

class Config:
    def __init__(self, state, head, tape):
        self.state = state
        self.head = head
        self.tape = tape

    def readSymbol(self, blank_symbol):
        if self.head == len(self.tape):
            self.tape = self.tape + blank_symbol
        return self.tape[self.head]

    def copyTape(self):
        return self.tape.copy()



class TuringMachine:
    def __init__(self, spec):
        self.states = spec[0]
        self.input_alphabet = spec[1]
        self.tape_alphabet = spec[2]
        self.start_symbol = spec[3]
        self.blank_symbol = spec[4]
        self.transitions = defaultdict(list) 
        for t in spec[5]:
            self.transitions[(t[0], t[1])].append((t[2], t[3], t[4]))
        self.initial_state = spec[6]
        self.final_states = set(spec[7])


    def simulate(self, word):
        visited = dict()
        config_inicial = Config(self.initial_state, 1, list(self.start_symbol + word + self.blank_symbol))
        queue = [config_inicial]
        visited.update({config_inicial:-1})

        while(len(queue) != 0):
            current_config = queue.pop(0)
            visited[current_config] = 1
            
            if((current_config.state in self.final_states) and (len(self.transitions[(current_config.state, current_config.head)])==0)):
                return True
            
            for next_state, new_symbol, direction in self.transitions[(current_config.state, current_config.readSymbol(self.blank_symbol))]:
                new_tape = current_config.copyTape()
                new_tape[current_config.head] = new_symbol 
                new_head = current_config.head + (1 if direction == '>' else -1)
                next_config = Config(next_state, new_head, new_tape)
                
                if visited.get(next_config, None) == None: visited[next_config] = -1
                if visited[next_config] == -1: 
                    queue.append(next_config)
                
        return False




def main():
    if len(sys.argv) != 3:
        print("Usar: python3 mt.py [MT] [Palavra]")
        return
    
    mt_file = sys.argv[1]
    word = sys.argv[2]
    with open(mt_file, 'r') as f:
        spec = json.load(f)["mt"]

    tm = TuringMachine(spec)
    if tm.simulate(word):
        print("Sim")
    else:
        print("Não") 



if __name__ == "__main__":
    main()