from music21 import *
# configure.run()
import numpy as np

class callAndResponse():
    def __init__(self, initCall):
        self.call = tuple(initCall)
        self.EPISODES = 1000
        self.Actions = ['UP', 'DOWN', 'FASTER', 'SLOWER', 'NONE']
        self.initScore = self.calculate_score(self.call)
        self.Q = {}
        for x in range(len(self.call)):
            self.Q[(self.call, x)] = [0, 0, 0, 0, 0]

        self.possible_notes = ["e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'"] 
        self.possible_rythems = ['4', '8', '16']
        self.rythem_values = {'4': 0.25, '8': 0.125, '16': 0.0625}
        
        self.response = self.sarsa()
        print(Q)

    def note_rythem(self, note):
        length = len(note)

        if "'" in note: 
            note2 = note[0:2]
            rythem = note[2:]
            print("rythem is: ", rythem)
        else: 
            note2 = note[0:1]
            rythem = note[1:]
        
        return (note2, rythem)

    def stochastic_note(self, note):      
        if "g":
             return np.random.choice(self.possible_notes, p=[0.13, 0.13, 0.13, 0.13, 0.13, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        if "a":
            return np.random.choice(self.possible_notes, p=[ 0.05, 0.13, 0.13, 0.13, 0.13, 0.13, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        if "b":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.13, 0.13, 0.13, 0.13, 0.13, 0.05, 0.05, 0.05, 0.05, 0.05])
        if "c'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.13, 0.13, 0.13, 0.13, 0.13, 0.05, 0.05, 0.05, 0.05])
        if "d'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.13, 0.13, 0.13, 0.13, 0.13, 0.05, 0.05, 0.05])
        if "e'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.13, 0.13, 0.13, 0.13, 0.13, 0.05, 0.05])
        if "f'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.13, 0.13, 0.13, 0.13, 0.13, 0.05])
        if "g'":
            return np.random.choice(self.possible_notes, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.13, 0.13, 0.13, 0.13, 0.13])

    def choose_rhythm(self):
        return np.random.choice(self.possible_rythems)

    def update_note(self, action, notePos, measure):
        currNote = measure[notePos]
        note, rythem = self.note_rythem(currNote)

        note_index = self.possible_notes.index(note)
        rythem_index = self.possible_rythems.index(rythem)

        if 'Up':
            if (note_index != len(self.possible_notes) - 1):
                newNote = self.possible_notes[note_index + 1]
            else:
                newNote = note
        if 'DOWN':
            if(note_index != 0):
                newNote = self.possible_notes[note_index - 1]
            else:
               newNote = note
        if 'FASTER':
            if(rythem_index != len(self.possible_rythems) - 1):
                newRythem = self.possible_rythems[rythem_index + 1]
            else: 
                newRythem = rythem
        if 'SLOWER':
            if(rythem_index != 0):
                newRythem = self.possible_rythems[rythem_index-1]
            else:
                newRythem = rythem

        return newNote + newRythem
    
    def change_measure(self, newNote, measure, notePos):
        measure[notePos] = newNote
        return measure

    def update_keys(self, newMeasure):
        x = 0
        for keys in Q.keys():
            self.Q[(newMeasure, x)] = self.Q[keys]
            del self.Q[keys]
            x += 1

    def choose_action(self, meas, pos):
        EPSILON = 0.2
        if np.random.rand() < EPSILON: 
            action = np.random.choice(self.Actions)
            action_ind = self.Actions.index(action)
            action_val = self.Q[meas, pos][action_ind]
        else:
            action_val = max(self.Q[meas, pos])
            action_index = self.Q[meas, pos].index(action_val) #gives me a corresponsing index
            action = self.Actions[action_index]

        return action, action_val

    def sarsa(self):
        currResponse = self.call 
        GAMMA = 0.9
        ALPHA = 0.1
        
        for episode in range(self.EPISODES):
            prevResponse = currResponse
            currNotePos = 0
            state = (prevResponse, currNotePos)
            action, action_val = self.choose_action(prevResponse, currNotePos)
            
            duration = 0
            while duration < 1: 
                alternative_action, alternative_action_val = self.choose_action(prevResponse, currNotePos)
                altMeasure = self.change_measure(self.update_note(alternative_action, currNotePos, prevResponse), list(prevResponse), currNotePos)
                alternative_action_val = self.calculate_score(prevResponse) - self.calculate_score(altMeasure)
                if alternative_action_val > action_val:
                    best_action = alternative_action
                else:
                    best_action = action
            
                newNote = self.update_note(best_action, currNotePos, currResponse) 
                note, rythem = self.note_rythem(newNote)
                currResponse = self.change_measure(newNote, list(currResponse), currNotePos)

                duration += self.rythem_values[rythem]
                currNotePos += 1

                state_prime = (prevResponse, currNotePos)
                action_prime, action_prime_val = self.choose_action(prevResponse, currNotePos)
                
                if self.calculate_score(currResponse) > self.calculate_score(prevResponse):
                    reward = 1
                else:
                    reward = 0
                
                best_index = self.Actions.index(best_action)
                index_prime = self.Actions.index(action_prime)
                self.Q[state][best_index] = self.Q[state][best_index] + ALPHA * (reward + GAMMA * self.Q[state_prime][index_prime] - self.Q[state][best_index])

            self.update_keys(currResponse)
        return currResponse

    def calculate_score(self, measure): 
        score = 0
        for i in range(len(measure) - 1):
            neighbor = ord(measure[i+1][0])   
            compare = ord(measure[i][0])
            # print(compare - neighbor)
            if abs(compare - neighbor) > 2:
               score -= score
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


    response = callAndResponse(call)
    res = list (response.getResponse())
    print(res)

    new_string = "tinynotation: 4/4"

    for note in call:
        new_string = new_string + " " + note

    for note in res:
        new_string = new_string + " " + note

    melody = converter.parse(new_string)
    melody.show()

if __name__ == "__main__" :
    main()