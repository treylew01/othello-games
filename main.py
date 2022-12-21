import sys
from agent import Greedy, Random
from trey import Trey
from fernando import Fernando
from game import play

class ReversiCLI():
    """Display board and questions."""
    def __init__(self, size, args):
        if size != 5:
            return

        self.total_games = float(args[4])
        self.time = float(args[3])


        if args[1] == "random":
            self.agent1 = Random(1)
        elif args[1] == "greedy":
            self.agent1 = Greedy(1)
        elif args[1] == "Fernando":
            self.agent1 = Fernando(self.time, 1)
        elif args[1] == "Trey":
            self.agent1 = Trey(self.time, 1)
        else:
            return

        if args[2] == "random":
            self.agent2 = Random(2)
        elif args[2] == "greedy":
            self.agent2= Greedy(2)
        elif args[2] == "Fernando":
            self.agent2 = Fernando(self.time, 2)
        elif args[2] == "Trey":
            self.agent2 = Trey(self.time, 2)
        else:
            return

        self.game = play


    def run(self):
        agent_score = 0.0
        count = 0
        while count < self.total_games:
            agent_score += self.game(self.agent1, self.agent2)
            count += 1
        #    print(agent_score/count)
        print(agent_score/self.total_games)


if __name__ == "__main__":
    try:
        argc = len(sys.argv)
        ReversiCLI(argc, sys.argv).run()

    except Exception as err:
        sys.exit(0)