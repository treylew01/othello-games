<h3 align="center">Othello Agent</h3>

  <p align="center">
    Final Project for CS474 
  </p>
  <p align="center">
    Fernando Salinas-Arreola & Trey Lewis
  </p>
  

## Getting Started

Just Python with The Base Libraries is needed

## Usage

To run the code use this command

python3 main.py agent1 agent2 seconds games

We named the agents we designed after ourselves, so the agents names are (case-sensitive):
- Fernando
- Trey
- random
- greedy 

The seconds argument is the time per move

The final argument games, is the number of games you want to play with the agent. 



A good example commands would be

python3 main.py Fernando random .2 50 \
python3 main.py Trey Fernando .2 50 \
python3 main.py greedy random .2 50 

<br>

The program as it stands will output the number of times player one WON, the program does not count draws or losses as a win. Therefore if you were to want to see which agent WINS the most, put that agent first

### Process 
We relied on an [online](https://inventwithpython.com/chapter15.html) resource to get started with the basic game functions. We had to heavliy change alot of this code to support our minimax functions as well as cut out a lot of code that was no longer neccessary

The idea was that we would both create our own agents and battle them against each other. We both went down the minimax route. We both developed our own algorithm and then ended up working on the final configuration of adding time together. Below are our approaches

### Trey
I first went down the minimax route, with a fixed depth, but I realized that if the user inputted a time, I wouldn't have control over that, therefore I used iterative deepening with minimax so that I could get deeper in the tree. I tested a few different heuristics, but I found that the heurisitic with assigning values to certain square and then adding up the pieces on those parts with the assigned values and then subtracting maximum - minimum worked best. This [paper](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf) outlines a supposedley better strategy, but do to time constraints with testing the other strategies, there wasn't enough time to change my strategy. 


### Fernando
I went down the alpha beta minimax method from the start with iterative deepening. My heurisitic took account of mobility of pieces (available moves), frontier pieces (pieces that are adjacent to empty spaces), the corners, and adjacent corners. I also have different strategies for different parts of the game. I penalize frontier score in the beginning and middle of the game, but do not account for it towards the end of the game. Towards the end of the game I emphasize game score and mobility so I can still have pieces to move. The weights also change depending on the phase of the game (early, mid, late) as the value of certain characteristics changes during the game (ex. in the early game total score does not matter but has a heavy emphasis during the late game). These could probably have been tuned more thoroughly to get the best perfromance out of this structure, but was still able to output interesting results.

## Results
- python3 main.py Fernando random 0.05 10000 - 0.846
- python3 main.py Trey greedy 0.05 10000 - 0.811
- python3 main.py Fernando Trey 0.01 10000 - 0.397
