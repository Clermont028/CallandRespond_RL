from music21 import *
# configure.run()
import numpy as np

class callAndResponse():
    def __init__(self, initCall):
        self.call = initCall
        self.EPISODES = 1000
        self.Actions = ['UP', 'DOWN', 'FASTER', 'SLOWER', 'NONE']
        self.initScore = self.calculate_score(self.call)
        self.Q = {}
        for x in range(16):
            self.Q[x] = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.possible_notes = ["e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'"] 
        self.possible_rythems = ['4', '8', '16']
        self.rythem_values = {'4': 0.25, '8': 0.125, '16': 0.0625}
        
        self.response = self.sarsa()

    def note_rythem(self, note):
        if "'" in note: 
            note2 = note[0:2]
            rythem = note[2:]
        else: 
            note2 = note[0:1]
            rythem = note[1:]
        
        return (note2, rythem)

    def stochastic_note(self, note):      
        if "g":
             return np.random.choice(self.possible_notes, p=[0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        if "a":
            return np.random.choice(self.possible_notes, p=[0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        if "b":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05, 0.05])
        if "c'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05])
        if "d'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05])
        if "e'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05])
        if "f'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05])
        if "g'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14])

    def choose_rhythm(self):
        return np.random.choice(self.possible_rythems)

    def update_note(self, action, notePos, measure):

        if notePos not in range(len(measure)):
            measure.append("")
            note, rythem = np.random.choice(self.possible_notes) , np.random.choice(self.possible_rythems)
        else:
            currNote = measure[notePos]
            note, rythem = self.note_rythem(currNote)   

        note_index = self.possible_notes.index(note)
        rythem_index = self.possible_rythems.index(rythem)

        newNote = note
        newRythem = rythem

        if action == 'UP':
            if note_index != len(self.possible_notes) - 1:
                newNote = self.possible_notes[note_index + 1]
        if action == 'DOWN':
            if  note_index != 0 :
                newNote = self.possible_notes[note_index - 1]

        if action == 'FASTER':
            if rythem_index != len(self.possible_rythems) - 1:
                newRythem = self.possible_rythems[rythem_index + 1]
        if action == 'SLOWER':
            if rythem_index != 0:
                newRythem = self.possible_rythems[rythem_index-1]

        return newNote + newRythem
    
    def change_measure(self, newNote, measure, notePos):
        measure[notePos] = newNote
        return measure

    def choose_action(self, meas, pos):
        EPSILON = 0.5
        if np.random.rand() < EPSILON: 
            action = np.random.choice(self.Actions)
            action_ind = self.Actions.index(action)
            action_val = self.Q[pos][action_ind]
        else:
            action_val = max(self.Q[pos])
            action_index = self.Q[pos].index(action_val) #gives me a corresponsing index
            action = self.Actions[action_index]

        return action, action_val

    def is_terminal(self, state, duration):
       return duration == 1 or state == 15

    def sarsa(self):
        currResponse = self.call 
        GAMMA = 0.1
        ALPHA = 0.1
        
        for episode in range(self.EPISODES):
            prevResponse = currResponse.copy()
            state = 0
            action, action_val = self.choose_action(prevResponse, state)
            
            duration = 0
            while self.is_terminal(state, duration) == False: 
                alternative_action, alternative_action_val = self.choose_action(prevResponse, state)
                alt_note = self.update_note(alternative_action, state, prevResponse)
                altMeasure = self.change_measure(alt_note, prevResponse, state)
                alternative_action_val =  self.calculate_score(prevResponse) - self.calculate_score(altMeasure) 

                if alternative_action_val > action_val:
                    best_action = alternative_action
                else:
                    best_action = action


                newNote = self.update_note(best_action, state, currResponse) 
                note, rythem = self.note_rythem(newNote)
                currResponse = self.change_measure(newNote, currResponse, state)

                duration += self.rythem_values[rythem]

                state_prime = state + 1
                action_prime, action_prime_val = self.choose_action(prevResponse, state_prime)
                
                if self.calculate_score(currResponse) > self.calculate_score(prevResponse):
                    reward = 1
                else:
                    reward = 0
                
                best_index = self.Actions.index(best_action)
                index_prime = self.Actions.index(action_prime)
                update = self.Q[state][best_index] + ALPHA * (reward +  GAMMA * self.Q[state_prime][index_prime] - self.Q[state][best_index])
                self.Q[state][best_index] = update
                
                state = state_prime
                action = action_prime

        return currResponse

    def calculate_score(self, measure): 
        score = 0
        for i in range(len(measure) - 1):
            neighbor = ord(measure[i+1][0])   
            compare = ord(measure[i][0])
            if abs(compare - neighbor) > 2:
               score -= 1

            note, rythem = self.note_rythem(measure[i])
            note2, rythem2 = self.note_rythem(measure[i+1])

            if rythem == '8' and rythem2 == '8':
                score += 1
            if rythem == '16' and rythem2 == '16':
                score += 1
    
        return score

    def getScore(self):
        return self.initScore

    def getResponse(self):
        return self.response

def main():
    call_str = input("Enter a measure: ")
    call_str = call_str.strip()
    call = call_str.split()
    print(call)

    new_string = "tinynotation: 4/4"

    for note in call:
        new_string = new_string + " " + note

    response = callAndResponse(call)
    res = list (response.getResponse())
    print(res)

    for note2 in res:
        new_string = new_string + " " + note2

    print(new_string)
    melody = converter.parse(new_string)
    melody.show()

if __name__ == "__main__" :
    main()