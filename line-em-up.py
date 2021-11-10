class Game:
    def __init__(self, recommend=True, n=3, b=0, s=3):
        self.initialize_game()
        self.recommend = recommend
        self.n = n
        self.b = b
        self.s = s

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
    ##Ask the user to input an n, b, and s and send them into this constructor
    g = Game(recommend=True)

if __name__ == "__main__":
    main()