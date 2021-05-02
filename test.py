from music21 import *
# configure.run()
import numpy as np

class callAndResponse():
    def __init__(self, initCall):
        self.call = initCall
        self.measure = self.call[0]
        self.call.pop(0)


        self.initScore = self.calculate_score(self.call)
        self.response = self.algorithm(self.call)

        # print(self.initScore)
      

    def stochastic_note(self, note):
        possible_notes = ['f4', 'g4', 'a', 'b', 'c', 'd', 'e', 'f', 'g5', 'a5', 'b5']

        if 'a':
            return np.random.choice(possible_notes, 1, p=[0.11, 0.11, 0.11, 0.11, 0.11, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075])
        if 'b':
            return np.random.choice(possible_notes, 1, p=[0.075, 0.11, 0.11, 0.11, 0.11, 0.11, 0.075, 0.075, 0.075, 0.075, 0.075])
        if 'c':
            return np.random.choice(possible_notes, 1, p=[0.075, 0.075, 0.11, 0.11, 0.11, 0.11, 0.11, 0.075, 0.075, 0.075, 0.075])
        if 'd':
            return np.random.choice(possible_notes, 1, p=[0.075, 0.075, 0.075, 0.11, 0.11, 0.11, 0.11, 0.11, 0.075, 0.075, 0.075])
        if 'e':
            return np.random.choice(possible_notes, 1, p=[0.075, 0.075, 0.075, 0.075, 0.11, 0.11, 0.11, 0.11, 0.11, 0.075, 0.075])
        if 'f':
            return np.random.choice(possible_notes, 1, p=[0.075, 0.075, 0.075, 0.075, 0.075, 0.11, 0.11, 0.11, 0.11, 0.11, 0.075])
        if 'g':
            return np.random.choice(possible_notes, 1, p=[0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.11, 0.11, 0.11, 0.11, 0.11])

        
    def choose_rhythm(self):
        return np.random.choice(['4', '8', '16'])

    def change(self, note):
       
       
        note = self.stochastic_note(note)
        rhythm = self.choose_rhythm()
        new_note = note + rhythm

        return new_note

    def algorithm(self, call):
        improved_score = self.initScore
        call = self.call
        response = []
        final = []

        while improved_score < 0:
            for note in call:
                new_note = self.change(note)
                response.append(new_note)

            response_score = self.calculate_score(response)
            improved_score = response_score - improved_score
            call = response
            final = response
            response = []
      
        self.response = final
        return self.response
                
    def calculate_score(self, measure):
        score = 0
        for i in range(len(measure) - 1):
            neighbor = ord(measure[i+1][0])   
            compare = ord(measure[i][0])
            # print(compare - neighbor)
            if abs(compare - neighbor) > 2:
               score -= 1
        return score

    def getScore(self):
        return self.initScore

    def getResponse(self):
        return self.response

def main():
    call_str = input("Enter a measure: ")
    call_str.strip()
    call = call_str.split(" ")
    print(call)

    response = callAndResponse(call)
    res = response.getResponse()

    print(res)
    new_string = "tinynotation: 3/4"

    # for note in res:
    #     new_string = new_string + " " + note

    # melody = converter.parse(new_string)
    # melody.show()



if __name__ == "__main__" :
    main()