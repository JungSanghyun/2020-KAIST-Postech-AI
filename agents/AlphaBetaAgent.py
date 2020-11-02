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


class AlphaBetaAgent(Agent):
    def __init__(self, maxDepth, player, adaptiveDepth=False):
        super(AlphaBetaAgent, self).__init__()
        self.maxDepth = maxDepth
        self.player = player
        self.adaptiveDepth = adaptiveDepth

    def _getAdaptiveDepth(self, state):
        numActions = len(state.possibleActions)
        maxDepth = 2
        if numActions < 25:
            maxDepth = 4
        elif numActions < 35:
            maxDepth = 3
        return maxDepth


    def _alphaBeta(self, state, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or state.isTerminal():
            return self._heuristicValue(state, depth), None

        chosenAction = None
        if maximizingPlayer:
            value = -sys.maxsize
            for action in state.possibleActions:
                child = state.step(action)
                childValue, _ = self._alphaBeta(child, depth - 1, alpha, beta, False)
                if value < childValue:
                    chosenAction = action
                    value = childValue
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, chosenAction

        else:
            value = sys.maxsize
            for action in state.possibleActions:
                child = state.step(action)
                childValue, _ = self._alphaBeta(child, depth - 1, alpha, beta, True)
                if value > childValue:
                    chosenAction = action
                    value = childValue
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, chosenAction

    def _heuristicValue(self, state, depth):
        if state.isTerminal():
            if state.winner() == self.player:
                return 100 * (self.maxDepth + 1) + depth
            else:
                return -100 * (self.maxDepth + 1) + depth

        playerScore, enemyScore = 0, 0
        for i in range(7):
            for j in range(7):
                if state.board[i][j] == self.player:
                    playerScore += 1
                elif state.board[i][j] == 3 - self.player:
                    enemyScore += 1
        return (playerScore - enemyScore) * (self.maxDepth + 1) + depth

    def getAction(self, state):
        if self.adaptiveDepth:
            self.maxDepth = self._getAdaptiveDepth(state)
        
        _, action = self._alphaBeta(state, self.maxDepth, -sys.maxsize, sys.maxsize, True)
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

        agent = AlphaBetaAgent(maxDepth=3, player=player, adaptiveDepth=True)
        action = agent.getAction(state=state)

        sys.stdout.write("{} {} {} {}" .format(*action))
