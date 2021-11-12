import string
import numpy as np
import time

debug = []

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    #X_PLAYER = '◦'
    #O_PLAYER = '•'
    X_PLAYER = 'X'
    O_PLAYER = 'O'
    BLOCK = "-"

    def __init__(self, recommend=True, n=3, b=0, s=3):
        self.current_state = []
        self.recommend = recommend
        self.blocks = []
        self.n = 0
        self.b = 0
        self.s = 0
        self.d1 = 0
        self.d2 = 0
        self.t = 0
        self.alphabeta = self.ALPHABETA
        self.p1 = self.HUMAN
        self.p2 = self.HUMAN
        self.recommend = True
        self.aDict = dict(zip(string.ascii_uppercase, range(0, 10)))
        self.bDict = dict(zip(range(0,10), string.ascii_uppercase))
        self.initialize_game()

    def initialize_game(self):
        valid = False
        while (not valid):
            self.n = int(input("Give a value n for the size of the board"))
            self.b = int(input("Give a value b for the amount of blocs to place on the board"))
            self.s = int(input("Give a value s for the amount of connecting positions must connect for a win"))
            self.d1 = int(input("Give a value d1 for the max depth of the algorithms for player 1"))
            self.d2 = int(input("Give a value d2 for the max depth of the algorithms for player 2"))
            self.t = int(input("Give a value t for the max time the algorithms may take for finding a move:"))
            self.alphabeta = int(input("Enter 1 to use alphabeta and enter 0 to use minimax"))
            self.p1 = int(input("Enter 2 for player 1 to be human or 3 for player 1 to be AI"))
            self.p2 = int(input("Enter 2 for player 2 to be human or 3 for player 2 to be AI"))
            rec = int(input("Enter 0 to have recommendations off or 1 to have recommendations off"))
            if rec == 0:
                self.recommend = False
            else:
                self.recommend = True
            for i in range(self.b):
                x_str = input(f"Enter the column of the {i + 1}th  block:")
                x = self.aDict[x_str]
                y = int(input(f"Enter the row of the {i + 1}th  block:"))
                self.blocks.append((y, x))
            if 3 <= self.n <= 10 and 0 <= self.b <= 2 * self.n and 3 <= self.s <= self.n:
                valid = True
            else:
                print("The given values were not valid, make sure that the following conditions are met:")
                print("n is an integer between 3 and 10 inclusive [3,...,10]")
                print("b is an integer between 0 and 2n inclusive [0,...,2n]")
                print("s is an integer between 3 and n inclusive [3,...,n]")
            print("------------------------------------------------------------------------------------------")
        for i in range(self.n):
            temp = []
            for j in range(self.n):
                temp.append('.')
            self.current_state.append(temp)

        for block_coordinates in self.blocks:
            self.current_state[block_coordinates[0]][block_coordinates[1]] = self.BLOCK

        self.player_turn = self.X_PLAYER

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[y][x]}', end="")
            print()
        print()

    def get_submatrices(self, state):
        slices = []
        for i in range(0, self.n - self.s + 1):
            for j in range(0, self.n - self.s + 1):
                slices.append(
                    [
                        [state[a][b] for b in range(j, j + self.s)]
                        for a in range(i, i + self.s)
                    ]
                )
        return slices

    def is_valid(self, px, py):
        if px < 0 or px >= self.n or py < 0 or py >= self.n:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        sub_matrices = self.get_submatrices(self.current_state)
        for sub in sub_matrices:
            # Diagonal win
            lr_diag = [row[i] for i, row in enumerate(sub)]
            is_win, winner = self.is_sub_win(lr_diag)
            if (is_win): return winner
            rl_diag = [row[-i - 1] for i, row in enumerate(sub)]
            is_win, winner = self.is_sub_win(rl_diag)
            if (is_win): return winner

            # Vertical win
            for i in range(self.s):
                col = [row[i] for row in sub]
                is_win, winner = self.is_sub_win(col)
                if (is_win): return winner

            # Horizontal win
            for row in sub:
                is_win, winner = self.is_sub_win(row)
                if (is_win): return winner

        # Is whole board full?
        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def is_sub_win(self, arr):
        items = set(arr)
        if len(items) == 1 and "." not in items and self.BLOCK not in items:
            return True, items.pop()
        return False, None

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == self.X_PLAYER:
                print(f'The winner is {self.X_PLAYER}!')
            elif self.result == self.O_PLAYER:
                print(f'The winner is {self.O_PLAYER}!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def e1(self, state):
        total = 0

        # row
        for row in state:
            for element in row:
                if element == self.X_PLAYER:
                    total += 1
                if element == self.O_PLAYER:
                    total -= 1

        # column
        for i in range(self.n):
            col = [row[i] for row in state]
            for element in col:
                if element == self.X_PLAYER:
                    total += 1
                if element == self.O_PLAYER:
                    total -= 1

        # diagonal
        valid_diagonals = self.get_valid_diags(state, self.s)
        for diagonal in valid_diagonals:
            for element in diagonal:
                if element == self.X_PLAYER:
                    total += 1
                if element == self.O_PLAYER:
                    total -= 1

        return total

    def e2(self, state):
        possible_wins = []
        score = 0
        # maximize for X_PLAYER
        sub_matrices = self.get_submatrices(state)
        for sub in sub_matrices:
            # Diagonals
            lr_diag = [row[i] for i, row in enumerate(sub)]
            rl_diag = [row[-i - 1] for i, row in enumerate(sub)]
            possible_wins.append(lr_diag)
            possible_wins.append(rl_diag)

        # Columns
        columns = []
        for i in range(self.n):
            col = [row[i] for row in state]
            columns.append(col)
        for col in columns:
            for i in range(self.n - self.s + 1):
                baby_column = []
                for j in range(i, i + self.s):
                    baby_column.append(col[j])
                possible_wins.append(baby_column)

        # Rows
        for row in state:
            for i in range(self.n - self.s + 1):
                baby_row = []
                for j in range(i, i + self.s):
                    baby_row.append(row[j])
                possible_wins.append(baby_row)

        for lst in possible_wins:
            if self.O_PLAYER in lst and self.X_PLAYER not in lst and self.BLOCK not in lst and lst.count(
                    self.O_PLAYER) == self.s:
                return 1000
            if self.X_PLAYER in lst and self.O_PLAYER not in lst and self.BLOCK not in lst and lst.count(
                    self.X_PLAYER) == self.s:
                return -1000
            elif self.O_PLAYER in lst and self.X_PLAYER not in lst and self.BLOCK not in lst:
                score += lst.count(self.O_PLAYER)
            elif self.X_PLAYER in lst and self.O_PLAYER not in lst and self.BLOCK not in lst:
                score -= lst.count(self.X_PLAYER)

        return score

    def minimax(self, depth, maximum=False):
        if maximum:
            x = None
            y = None
            value = -10000
            for i in range(self.n):
                for j in range(self.n):
                    if self.current_state[i][j] == '.':
                        self.current_state[i][j] = self.player_turn
                        if depth == 0 or self.is_terminal_node():
                            v = self.e2(self.current_state)
                            self.current_state[i][j] = '.'
                            return (v, j, i)
                        (v, _, _) = self.minimax(depth-1, False)
                        if v > value:
                            x = j
                            y = i
                            value = v
                        self.current_state[i][j] = '.'
            return (value, x, y)
        else:
            x = None
            y = None
            value = 10000
            for i in range(self.n):
                for j in range(self.n):
                    if self.current_state[i][j] == '.':
                        self.current_state[i][j] = self.player_turn
                        if depth == 0 or self.is_terminal_node():
                            v = self.e2(self.current_state)
                            self.current_state[i][j] = '.'
                            return (v, j, i)
                        (v, _, _) = self.minimax(depth - 1, True)
                        if v < value:
                            x = j
                            y = i
                            value = v
                        self.current_state[i][j] = '.'
            return (value, x, y)

    def is_terminal_node(self):
        full = True
        for row in self.current_state:
            if '.' in row:
                full = False

        return full


    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == self.X_PLAYER:
                    (_, x, y) = self.minimax(self.d1, maximum=False)
                else:
                    (_, x, y) = self.minimax(self.d2, maximum=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == self.X_PLAYER:
                    (m, x, y) = self.alphabeta(maximum=False)
                else:
                    (m, x, y) = self.alphabeta(maximum=True)
            end = time.time()
            if (self.player_turn == self.X_PLAYER and player_x == self.HUMAN) or (
                    self.player_turn == self.O_PLAYER and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {self.bDict[x]}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == self.X_PLAYER and player_x == self.AI) or (
                    self.player_turn == self.O_PLAYER and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {self.bDict[x]}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            x_str = input('enter the x coordinate: ')
            px = self.aDict[x_str]
            py = int(input('enter the y coordinate: '))
            if self.is_valid(py, px):
                return (py, px)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == self.X_PLAYER:
            self.player_turn = self.O_PLAYER
        elif self.player_turn == self.O_PLAYER:
            self.player_turn = self.X_PLAYER
        return self.player_turn

    def get_valid_diags(self, state, s):
        state = np.array(state)
        diags = [state[::-1, :].diagonal(i) for i in range(-state.shape[0] + 1, state.shape[1])]
        diags.extend(state.diagonal(i) for i in range(state.shape[1] - 1, -state.shape[0], -1))
        valid_diagonals = []

        for diag in diags:
            if diag.shape[0] < s:
                continue
            valid_diagonals.append(diag)

        return [n.tolist() for n in valid_diagonals]


def main():
    g = Game(recommend=True)
    g.play(algo=g.alphabeta, player_x=g.p1, player_o=g.p2)


if __name__ == "__main__":
    main()
