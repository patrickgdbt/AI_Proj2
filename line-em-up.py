import string
import numpy as np

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    X_PLAYER = '◦'
    O_PLAYER = '•'

    def __init__(self, recommend=True, n=3, b=0, s=3):
        self.current_state = []
        self.recommend = recommend
        self.blocks = []
        self.n = 0
        self.b = 0
        self.s = 0
        self.aDict = dict(zip(string.ascii_uppercase, range(0, 10)))
        self.initialize_game()

    def initialize_game(self):
        valid = False
        while (not valid):
            self.n = int(input("Give a value n for the size of the board"))
            self.b = int(input("Give a value b for the amount of blocs to place on the board"))
            self.s = int(input("Give a value s for the amount of connecting positions must connect for a win"))
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
            self.current_state[block_coordinates[0]][block_coordinates[1]] = "☒"

        # self.n = 5
        # self.s = 3
        # self.b = 4
        # test = [['☒', '◦', '.', '◦', '.'],
        #         ['.', '☒', '.', '☒', '•'],
        #         ['.', '•', '.', '◦', '.'],
        #         ['.', '.', '.', '.', '.'],
        #         ['.', '◦', '☒', '.', '•']]
        # print(self.e1(test))

        self.player_turn = self.X_PLAYER

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[x][y]}', end="")
            print()
        print()

    def get_submatrices(self):
        slices = []
        for i in range(0, self.n - self.s + 1):
            for j in range(0, self.n - self.s + 1):
                slices.append(
                    [
                        [self.current_state[a][b] for b in range(j, j + self.s)]
                        for a in range(i, i + self.s)
                    ]
                )
        return slices

    def is_end(self):
        sub_matrices = self.get_submatrices()
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
        if len(items) == 1 and "." not in items and "☒" not in items:
            return True, items.pop()
        return False, None

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == self.X_PLAYER:
                print('The winner is ◦!')
            elif self.result == self.O_PLAYER:
                print('The winner is •!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def e1(self, state):
        total = 0
        #row
        for row in state:
            for element in row:
                if element == self.X_PLAYER:
                    total += 1
                if element == self.O_PLAYER:
                    total -= 1

        #column
        for i in range(self.n):
            col = [row[i] for row in state]
            for element in col:
                if element == self.X_PLAYER:
                    total += 1
                if element == self.O_PLAYER:
                    total -= 1

        #diagonal
        valid_diagonals = self.get_valid_diags(state)
        for diagonal in valid_diagonals:
            for element in diagonal:
                if element == self.X_PLAYER:
                    total += 1
                if element == self.O_PLAYER:
                    total -= 1

        return total

    def e2(self, state):
        # maximize for X_PLAYER
        return

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
                (_, x, y) = self.minimax(max=False)
            else:
                (_, x, y) = self.minimax(max=True)
        else:  # algo == self.ALPHABETA
            if self.player_turn == self.X_PLAYER:
                (m, x, y) = self.alphabeta(max=False)
            else:
                (m, x, y) = self.alphabeta(max=True)
        end = time.time()
        if (self.player_turn == self.X_PLAYER and player_x == self.HUMAN) or (
                self.player_turn == '•' and player_o == self.HUMAN):
            if self.recommend:
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Recommended move: x = {x}, y = {y}')
            (x, y) = self.input_move()
        if (self.player_turn == self.X_PLAYER and player_x == self.AI) or (
                self.player_turn == '•' and player_o == self.AI):
            print(F'Evaluation time: {round(end - start, 7)}s')
            print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
        self.current_state[x][y] = self.player_turn
        self.switch_player()

    def switch_player(self):
        if self.player_turn == self.X_PLAYER:
            self.player_turn = self.O_PLAYER
        elif self.player_turn == self.O_PLAYER:
            self.player_turn = self.X_PLAYER
        return self.player_turn

    def get_valid_diags(self, state):
        state = np.array(state)
        diags = [state[::-1, :].diagonal(i) for i in range(-state.shape[0] + 1, state.shape[1])]
        diags.extend(state.diagonal(i) for i in range(state.shape[1] - 1, -state.shape[0], -1))
        valid_diagonals = []

        for diag in diags:
            if diag.shape[0] < self.s:
                continue
            valid_diagonals.append(diag)

        return [n.tolist() for n in valid_diagonals]


def main():
    g = Game(recommend=True)


if __name__ == "__main__":
    main()
