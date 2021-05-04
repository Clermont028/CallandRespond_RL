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
- **Problem:** When given a user-generated **call**, can a program output an adequate **response** that both reflects and creatively builds off the original?
- **States:** Note position within a measure
- **Rewards:** If a changed measure (response) has a score greater than a previously inputted measure (call) then it earns a reward of 1, otherwise -1.
  
| Actions | Description |
| ------------- | ------------- |
| **UP**  | move current note one note up  |
| **DOWN** | move current note one note down  |
| **FASTER** | select a "faster" rhythm (ex. changing an 8th note to a 16th)  |
| **SLOWER** | select a "slower" rhythm, (ex. changing an 8th note to a quarter)  |
| **NONE** | no changes made |

### Part 2
- **What is your algorithm learning?**
  - Our algorithm is learning what actions are the best to take to "improve" and build off a given call.
- **Do you have a success metric?** (e.g. wins a game 80% of the time, achieves a score of 500, etc.)
  - There is no success metric. Creativity is purely subjective, therefore it was up to us, personally, to determine whether or not a result qualified as "good" or not.
  - In tandem with this notion, we've made it so that no call will yield a single "best" result. Each time the program is run with the same inputted call, a unique response will always be returned.

### Part 3
- **The learning algorithm(s) you used in solving the problem.**
  - SARSA
- **Why do you think this was an appropriate choice?**
  - For our project, we needed an algorithm that would be able to learn while it explored the model-free environment. It was also important to use an algorithm that considered state-action pairs rather than only state-values because our program is more reliant on making adjustments that gradually improve the overall music rather than making the best decision, so state-values alone wouldn't help us determine what would be a better improvement to make.

### Results
 - **Explaing the values of the applicable hyperparameters (alpha, gamma, epsilon) you used. How did you decide what values to use?**
   -  alpha: we used a standard alpha of 0.1 as we had no preference regarding its learning rate 
   -  gamma: [debating]
   -  epsilon: we increased the epsilon to 0.5 so that it have a higher chance to explore other options (and thus align itself more with the creative process)
 - **Support your results through graphs, if applicable. How did you decide that the algorithm converged?**
   - Given there's no "right" answer, there's no optimal policy to be expected. Even if given the same input by the user, the program will always output something unique in return. Therefore, there is no convergence that can occur. Instead, we judge the score of the final result is greater than the original input. 
 - **A few screenshots of your problem/game to describe how your agent works**
   - First iteration (original call is in the first measure):
   ![image](https://user-images.githubusercontent.com/48339547/117077260-63713900-acfd-11eb-8c0e-a332564a7f00.png)
   - Final iteration:
   ![image](https://user-images.githubusercontent.com/48339547/117077351-90bde700-acfd-11eb-9f00-78d700a23010.png)
   
# Conclusion
- **A brief summary of your results**
  - Overall, we were surprised by how well the program performed in the end. Given our lack of musical background, it was interesting to see the program output a result that was sounded sufficiently pleasing to the human ear.
- **What did you learn from this project?**
  - From this project, we learned that creativity is quite a difficult and ambitious endeavor to emulate through a computer program. Especially now, after completing the program, we realize there is still so much more that could be added to fully encapsulate a more holistic musical response. 
  - During our main testing stage, we also did experience many instances in which our program learned to high-jack and game the reward system, so that was fun.
  - We also learned a lot during our time figuring out which parameters we needed to adjust to generate more appropriate responses. 
- **What was the most challenging part?**
  - It took us 3 hours to download and and figure out how to get Music21 to work on vscode :)
  - Developing the algorithm: we went through many iterations trying to figure out what the states should be, how to reward/score the measures
- **What would you add/research if you had the opportunity to continue this work?**
  - Less user-input restrictions :)
  - More sophisticated scoring of measures
  - Research of and utilization of tendency tones to help ensure that measures ended on notes that feel more "conclusive"
  - Have the program be able to continuously build off responses to produce a whole song/piece
  - More research on what exactly makes music sound "good" from a mathematical standpoint
  - A very lofty goal, but our original idea was to first implement call-and-response in relation to music and then eventually translate that to how call-and-response works in everyday huamn speech.

# References

