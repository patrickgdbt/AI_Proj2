class Game:
    def __init__(self, recommend=True, n=3, b=0, s=3):
        self.initialize_game()
        self.recommend = recommend


    def initialize_game(self):
        valid = False
        while (not valid):
            self.n = int(input("Give a value n for the size of the board"))
            self.b = int(input("Give a value b for the amount of blocs to place on the board"))
        ##somewhere here we gotta ask for the coordinates that we want to put the "blocs" in
            self.s = int(input("Give a value s for the amount of connecting positions must connect for a win"))
            if 3 <= self.n <= 10 and 0 < self.b <= 2 * self.n and 3 <= self.s <= self.n:
                valid = True
            else:
                print("The given values were not valid, make sure that the following conditions are met:")
                print("n is an integer between 3 and 10 inclusive [3,...,10]")
                print("b is an integer between 0 and 2n inclusive [0,...,2n]")
                print("s is an integer between 3 and n inclusive [3,...,n]")
            print("------------------------------------------------------------------------------------------")
        self.current_state = [['.', '.', '.'],
                              ['.', '.', '.'],
                              ['.', '.', '.']]
        # Player X always plays first
        self.player_turn = 'X'

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
            if self.player_turn == 'X':
                (_, x, y) = self.minimax(max=False)
            else:
                (_, x, y) = self.minimax(max=True)
        else:  # algo == self.ALPHABETA
            if self.player_turn == 'X':
                (m, x, y) = self.alphabeta(max=False)
            else:
                (m, x, y) = self.alphabeta(max=True)
        end = time.time()
        if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
            if self.recommend:
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Recommended move: x = {x}, y = {y}')
            (x, y) = self.input_move()
        if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
            print(F'Evaluation time: {round(end - start, 7)}s')
            print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
        self.current_state[x][y] = self.player_turn
        self.switch_player()


def main():
    g = Game(recommend=True)

if __name__ == "__main__":
    main()
