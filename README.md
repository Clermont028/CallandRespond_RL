# CallandRespond_RL
Team Members: Bernadette Clermont and Alyssa Pham
# Description
CallandRespond_RL is a music-based learning program that attempts to mimic the call-and-response technique.
- In music, one player offers a phrase that the second player then builds off of and provides unique commentary to. The primary objective is for both musicians to work together to help move the song along in a way that is both creative and cohesive.
## How to Use
### Important
- Prior to running the code, it is best to ensure you have the proper configurations set up. 
- In our program, we've utilized the Python-based toolkit **Music21** from MIT to help generate and compose our musical examples. 
  - [More information can be found through their documentation website.](http://web.mit.edu/music21/doc/index.html)
- This toolkit is compatible with music notation software such as [LilyPond](http://lilypond.org/), [Finale](https://www.finalemusic.com/), and [MuseScore](https://musescore.org/en). To be able to display the results of our program, we recommend you download one of these three options (we've personally used MuseScore).
### User Input
- Though Music21 is quite robust, for the sake of this project, we have taken the liberty of imposing limitations on what is considered 'valid' input by the user. This is just to ensure we are not working with an overly large and complex state-action space.
- **8-note limitation**
  - User may choose from a set of 8 possible notes (as shown in the image below)
  - Code representation: g, a, b, c', d', e', f', g'  (Note: an apostrophe following a letter indicates that the note occupies a different octave) 
  ![image](https://user-images.githubusercontent.com/48339547/116928339-8c70cb80-ac22-11eb-84d3-4e569ff2641c.png)
- **Rhythm limitation**
  - User may choose from a set of 3 possible rhythms (rests not included): quarter, eighth, 16th
  - Code representation: 4, 8, 16 (follows after chooosing the note)
  ![image](https://user-images.githubusercontent.com/48339547/116947073-6eff2a00-ac41-11eb-8339-b092f7b8f658.png)

- **No sharp/flat/etc. indicators**
- **Assumption that the user will always be working in a 4/4 time signature**

## Breakdown of Algorithm 
### Part 1
- Describe the problem, states, actions, rewards
- Problem: When given a user-generated **call**, can a program output an adequate **response** that both reflects and creatively builds off the original?
  - States: Note position within a measure
First Header | Second Header
------------ | -------------
Content from cell 1 | Content from cell 2
Content in the first column | Content in the second column
- What is your algorithm learning?
- Do you have a success metric? (e.g. wins a game 80% of the time, achieves a score of 500, etc.)

- The learning algorithm(s) you used in solving the problem.
- Why do you think this was an appropriate choice?

- Results
  - Explaing the values of the applicable hyperparameters (alpha, gamma, epsilon) you used. How did you decide what values to use?
  - Support your results through graphs, if applicable. How did you decide that the algorithm converged?
  - A few screenshots of your problem/game to describe how your agent works
# Conclusion
- A brief summary of your results
- What did you learn from this project?
- What was the most challenging part?
- What would you add/research if you had the opportunity to continue this work?

# References

