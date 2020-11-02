import sys
import random
import copy

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


class RuleBasedAgent(Agent):
    def __init__(self, player):
        super(RuleBasedAgent, self).__init__()
        self.player = player

    def getAction(self, state):
        actions_possible = {}
        enemy = 3 - state.turn
        for action in state.possibleActions:
            a, b, x, y = action
            if (a, b) in actions_possible.keys():
                actions_possible[(a, b)].append((x, y))
            else:
                actions_possible[(a, b)] = [(x, y)]
        max_eating = 0
        max_actions = {}
        max_damage_actions = {}
        for position, actions in list(actions_possible.items()):
            max_action_list = []
            max_damage_action_list = []
            for action in actions:
                move = False
                eating = 0
                if abs(position[0] - action[0]) == 2 or abs(position[1] - action[1]) == 2:
                    eating -= 1
                    for i in range(max(position[0] - 2, 0), min(position[0] + 3, 7)):
                        for j in range(max(position[1] - 2, 0), min(position[1] + 3, 7)):
                            if state.board[i][j] == enemy:
                                enemy_eating = 0
                                move = True
                for i in range(max(action[0] - 1, 0), min(action[0] + 2, 7)):
                    for j in range(max(action[1] - 1, 0), min(action[1] + 2, 7)):
                        if state.board[i][j] == enemy:
                            eating += 1
                if move:
                    for i in range(max(position[0] - 1, 0), min(position[0] + 2, 7)):
                        for j in range(max(position[1] - 1, 0), min(position[1] + 2, 7)):
                            if state.board[i][j] == player:
                                enemy_eating += 1
                    if eating <= enemy_eating and eating == max_eating:
                        max_damage_action_list.append(action)
                        continue
                if eating == max_eating:
                    max_action_list.append(action)
                if eating > max_eating:
                    max_eating = eating
                    max_actions = {}
                    max_action_list = [action]
                    max_damage_action_list = []
            if max_action_list:
                max_actions[position] = max_action_list
                max_damage_actions[position] = max_damage_action_list

        if list(max_actions.items()):
            piece, positions = random.choice(list(max_actions.items()))
            position = random.choice(positions)
        else:
            piece, positions = random.choice(list(max_damage_actions.items()))
            position = random.choice(positions)

        action_final = (piece[0], piece[1], position[0], position[1])
        return action_final

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

        agent = RuleBasedAgent(player=player)
        action = agent.getAction(state=state)

        sys.stdout.write("{} {} {} {}" .format(*action))
