# -*- coding: utf-8 -*-
import sys
import copy
import random


class AtaxxState(object):
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn
        self.possibleActions = None
        self._updatePossibleActions()

    def _updatePossibleActions(self):
        possibleActions = []
        dupDirection = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        movDirection = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, 2), (0, -2),
                        (0, 2), (1, -2), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]

        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 0:
                    for direction in dupDirection:
                        x, y = i + direction[0], j + direction[1]
                        if 0 <= x < 7 and 0 <= y < 7 and self.board[x][y] == self.turn:
                            possibleActions.append((x, y, i, j))
                            break

        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 0:
                    for direction in movDirection:
                        x, y = i + direction[0], j + direction[1]
                        if 0 <= x < 7 and 0 <= y < 7 and self.board[x][y] == self.turn:
                            possibleActions.append((x, y, i, j))
        self.possibleActions = possibleActions

    def step(self, action):
        x, y, i, j = action

        board = copy.deepcopy(self.board)
        board[i][j] = self.turn
        if abs(x - i) == 2 or abs(y - j) == 2:
            board[x][y] = 0

        for k in range(max(0, i - 1), min(7, i + 2)):
            for l in range(max(0, j - 1), min(7, j + 2)):
                if board[k][l] == 3 - self.turn:
                    board[k][l] = self.turn

        turn = 3 - self.turn
        nextState = AtaxxState(board=board, turn=turn)
        return nextState

    def isTerminal(self):
        return len(self.possibleActions) == 0

    def winner(self):
        playerScores = [None, 0, 0]
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == self.turn:
                    playerScores[self.turn] += 1
                else:
                    playerScores[3 - self.turn] += 1
        return 1 if playerScores[1] > playerScores[2] else 2


class Agent(object):
    def __init__(self):
        pass

    def getAction(self, state):
        pass


class RandomAgent(Agent):
    def __init__(self, randomSeed=None):
        super(RandomAgent, self).__init__()
        random.seed(randomSeed)

    def getAction(self, state):
        action = random.choice(state.possibleActions)
        return action


if __name__ == "__main__":
    input_str = sys.stdin.read()

    if input_str.startswith("READY"):
        sys.stdout.write("OK")
    
    elif input_str.startswith("PLAY"):
        player = int(__file__[2])
        board = []

        lines = input_str.split("\n")
        for i in range(7):
            line = list(map(lambda x: int(x), lines[i+1].split(" ")))
            board.append(line)

        state = AtaxxState(board=board, turn=player)

        agent = RandomAgent()
        action = agent.getAction(state=state)

        sys.stdout.write("{} {} {} {}" .format(*action))
