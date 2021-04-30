from music21 import *

class callAndResponse():
    def __init__(self, initCall):
        self.call = initCall
        self.measure = self.call[0]
        self.call.pop(0)

        self.initScore = self.score(self.call)
        print(self.initScore)

    def score(self, measure):
        score = 0
        for i in range(len(measure) - 1):
            neighbor = ord(measure[i+1])   
            compare = ord(measure[i][0])
            print(compare - neighbor)
            if abs(compare - neighbor) > 2:
                score -= 1
        return score

def main():
    call_str = input("Enter a measure: ")
    call_str.strip()
    call = call_str.split(" ")
    print(call)

    callAndResponse(call)

if __name__ == "__main__" :
    main()