from music21 import *
# ** ATTENTION **
# ** If this is your first time running the code, please be sure that you
# ** 1) Have the music21 package installed and
# ** 2) Have either LilyPond, Finale, or MuseScore on your device
# ** Once you have both, comment out all of the code below EXCEPT configure.run() and then run the program
# ** It will take a while to load, so please be patient. You can answer 'No' to all Y/N questions that it prompts

# configure.run()
import numpy as np


class callAndResponse():

    def __init__(self, initCall):

        self.call = initCall
        self.EPISODES = 1000

        self.ALL_POSSIBLE_ACTIONS = ['UP', 'DOWN', 'FASTER', 'SLOWER', 'NONE']
        self.ALL_POSSIBLE_NOTES = ["e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'"] 
        self.ALL_POSSIBLE_RHYTHMS = ['4', '8', '16']
        self.RHYTHM_VALUES = {'4': 0.25, '8': 0.125, '16': 0.0625} #used to calculate measure duration
        self.MAXDURATION = self.get_total_duration(self.call)

        self.ALPHA = 0.1
        self.GAMMA = 0.1
        self.EPSILON = 0.5

        self.initScore = self.calculate_score(self.call, self.MAXDURATION)

        # state-action-value dictionary
        # key = note position (index within measure)
        # value = list of values associated with a given action [UP, DOWN, FASTER, SLOWER, NONE]
        self.Q = {} 
        for x in range(16):
            self.Q[x] = [0.0, 0.0, 0.0, 0.0, 0.0]
    
        self.response = self.sarsa()


    def get_note_parts(self, note):

        if "'" in note: 
            letter = note[0:2]
            rhythm = note[2:]
        else: 
            letter = note[0:1]
            rhythm = note[1:]
        
        return (letter, rhythm)


    def get_total_duration(self, measure):
        total_duration = 0

        for i in range(len(measure)):
            note, rhythm = self.get_note_parts(measure[i]) 
            total_duration += self.RHYTHM_VALUES[rhythm]
        
        return total_duration


    def stochastic_note(self, note):  

        if note == "g":
             return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        if note == "a":
            return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        if note == "b":
            return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05, 0.05])
        if note == "c'":
            return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05, 0.05])
        if note == "d'":
            return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05, 0.05])
        if note == "e'":
            return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05, 0.05])
        if note == "f'":
            return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14, 0.05])
        if note == "g'":
            return np.random.choice(self.ALL_POSSIBLE_NOTES, p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.14, 0.14, 0.09, 0.14, 0.14])

   
    def stochastic_rhythm(self, rhythm):
        if rhythm == '4':
            return np.random.choice(self.ALL_POSSIBLE_RHYTHMS, p=[0.6, 0.3, 0.1])
        if rhythm == '8':
            return np.random.choice(self.ALL_POSSIBLE_RHYTHMS, p=[0.2, 0.6, 0.2])   
        if rhythm == '16':
            return np.random.choice(self.ALL_POSSIBLE_RHYTHMS, p=[0.1, 0.3, 0.6])


    def stochastic_action(self, action):
        if action == 'UP':
            return np.random.choice(self.ALL_POSSIBLE_ACTIONS, p=[0.7, 0.15, 0.05, 0.05, 0.05])
        if action == 'DOWN':
            return np.random.choice(self.ALL_POSSIBLE_ACTIONS, p=[0.15, 0.7, 0.05, 0.05, 0.05])
        if action == 'FASTER':
            return np.random.choice(self.ALL_POSSIBLE_ACTIONS, p=[0.05, 0.05, 0.7, 0.15, 0.05])
        if action == 'SLOWER':
            return np.random.choice(self.ALL_POSSIBLE_ACTIONS, p=[0.05, 0.05, 0.15, 0.7, 0.05])
        if action == 'NONE':
            return np.random.choice(self.ALL_POSSIBLE_ACTIONS, p=[0.05, 0.05, 0.05, 0.05, 0.8])

   
    def update_note(self, action, notePos, measure):
        """Performs a given action and returns the resulting note."""

        actual_action = self.stochastic_action(action)

        if notePos not in range(len(measure)):
            measure.append("")
            note, rhythm = np.random.choice(self.ALL_POSSIBLE_NOTES), np.random.choice(self.ALL_POSSIBLE_RHYTHMS)
        else:
            currNote = measure[notePos]
            note, rhythm = self.get_note_parts(currNote)   

        note_index = self.ALL_POSSIBLE_NOTES.index(note)
        rhythm_index = self.ALL_POSSIBLE_RHYTHMS.index(rhythm)

        newNote = note
        newRhythm = rhythm

        if actual_action == 'UP':
            if note_index != len(self.ALL_POSSIBLE_NOTES) - 1:
                newNote = self.ALL_POSSIBLE_NOTES[note_index + 1]

        if actual_action == 'DOWN':
            if  note_index != 0 :
                newNote = self.ALL_POSSIBLE_NOTES[note_index - 1]

        if actual_action == 'FASTER':
            if rhythm_index != len(self.ALL_POSSIBLE_RHYTHMS) - 1:
                newRhythm = self.ALL_POSSIBLE_RHYTHMS[rhythm_index + 1]

        if actual_action == 'SLOWER':
            if rhythm_index != 0:
                newRhythm = self.ALL_POSSIBLE_RHYTHMS[rhythm_index-1]

        return newNote + newRhythm 

    
    def change_measure(self, newNote, measure, notePos):
        """Updates the measure to include a newly made note."""

        measure[notePos] = newNote
        return measure


    def choose_action(self, measure, pos):
        """Chooses an action based on the epsilon-greedy method."""

        if np.random.rand() < self.EPSILON: 
            action = np.random.choice(self.ALL_POSSIBLE_ACTIONS)
            action_index = self.ALL_POSSIBLE_ACTIONS.index(action)
            action_value = self.Q[pos][action_index]

        else:
            action_value = max(self.Q[pos])
            action_index = self.Q[pos].index(action_value) # gives me a corresponsing index
            action = self.ALL_POSSIBLE_ACTIONS[action_index]

        return action, action_value


    def is_terminal(self, state, duration):
       return duration >= self.MAXDURATION or state == 15


    def sarsa(self):
        """Performs SARSA algorithm."""

        currResponse = self.call 
    
        for episode in range(self.EPISODES):
            prevResponse = currResponse.copy()  # prevResponse acts as the 'call'

            state = 0   # state = position of note within measure
            action, action_val = self.choose_action(prevResponse, state)
            duration = 0
           
            while self.is_terminal(state, duration) == False: 

                newNote = self.update_note(action, state, currResponse) 
                note, rhythm = self.get_note_parts(newNote)
                currResponse = self.change_measure(newNote, currResponse, state)

                duration += self.RHYTHM_VALUES[rhythm]

                state_prime = state + 1
                action_prime, action_prime_val = self.choose_action(prevResponse, state_prime)
                
                currScore = self.calculate_score(currResponse, duration)
                prevScore = self.calculate_score(prevResponse, duration)
                difference = abs(currScore - prevScore)

                if currScore > prevScore:
                    reward = difference
                else:
                    reward = -1

                action_index = self.ALL_POSSIBLE_ACTIONS.index(action)
                index_prime = self.ALL_POSSIBLE_ACTIONS.index(action_prime)
                update = self.Q[state][action_index] + self.ALPHA * (reward +  self.GAMMA * self.Q[state_prime][index_prime] - self.Q[state][action_index])
                self.Q[state][action_index] = update
                
                state = state_prime
                action = action_prime
            currResponse = currResponse[:state] 

        return currResponse


    def calculate_score(self, measure, duration): 
        score = 0

        for i in range(len(measure) - 1):

            note, rhythm = self.get_note_parts(measure[i])
            after, r_after = self.get_note_parts(measure[i+1])

            neighbor = ord(measure[i+1][0])   
            compare = ord(measure[i][0])

            # penalizes notes with large intervals between its neighbors
            if abs(compare - neighbor) > 2:
                score -= 2

            # rewards 8th and 16th notes that come in pairs
            # ex. it would be 'awkward' to have a quarter note jump to a lone 16th note
            if rhythm == '8' and r_after == '8':
                score += 1
            if rhythm == '16' and r_after == '16':
                score += 1


        return score


    def getScore(self):
        return self.initScore


    def getResponse(self):
        return self.response


def main():

    user_input = input("Enter a measure: ")
    user_input = user_input.strip()
    call = user_input.split()

    final = "tinynotation: 4/4"

    for note in call:
        final = final + " " + note

    response = callAndResponse(call)
    res = list(response.getResponse())

    for note2 in res:
        final = final + " " + note2

    # calls music notation software to display final result
    melody = converter.parse(final)
    melody.show()

if __name__ == "__main__" :
    main()