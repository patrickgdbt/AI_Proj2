import string
import numpy as np
import time
import random

debug = []


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    # X_PLAYER = '◦'
    # O_PLAYER = '•'
    X_PLAYER = 'X'
    O_PLAYER = 'O'
    BLOCK = "-"
    heuristic1_wins = 0
    heuristic2_wins = 0
    scoreboard_evaluation_times = []
    scoreboard_total_evaluations = []
    scoreboard_evaluations_by_depth = {}
    scoreboard_depths = []
    scoreboard_recursion_depth = []
    scoreboard_moves_per_game = []

    def __init__(self, recommend=True, n=3, b=0, s=3, d1=5, d2=5, t=5, blocks=[], a1=True, a2=True,
                 random_blocks=False, h1=1, h2=2):
        self.current_state = []
        self.random_blocks = random_blocks
        self.recommend = recommend
        self.blocks = blocks
        self.n = n
        self.b = b
        self.s = s
        self.d1 = d1
        self.d2 = d2
        self.t = t
        self.p1 = self.AI
        self.p2 = self.AI
        if a1:
            self.algo1 = self.ALPHABETA
        else:
            self.algo1 = self.MINIMAX
        if a2:
            self.algo2 = self.ALPHABETA
        else:
            self.algo2 = self.MINIMAX
        self.recommend = True
        self.heuristic1 = h1
        self.heuristic2 = h2
        self.time_heuristic1 = []
        self.time_heuristic2 = []
        self.count_heuristic1 = 0
        self.count_heuristic2 = 0
        self.per_move_average_1 = []
        self.per_move_average_2 = []
        self.total_depth_1 = {}
        self.total_depth_2 = {}
        self.total_moves_1 = 0
        self.total_moves_2 = 0
        self.visited = 0
        self.depthVisits = {}
        self.aDict = dict(zip(string.ascii_uppercase, range(0, 10)))
        self.bDict = dict(zip(range(0, 10), string.ascii_uppercase))
        self.average_recursive_depth = 0
        self.average_recursive_depths1 = []
        self.average_recursive_depths2 = []
        self.initialize_game()

    def initialize_game(self):
        if (False):
            self.get_console_input()

        if self.random_blocks:
            random_blocks = []
            for i in range(self.b):
                current_block = None
                while current_block not in random_blocks:
                    current_block = (random.randint(0, self.n - 1), random.randint(0, self.n - 1))
                    random_blocks.append(current_block)
            self.blocks = random_blocks

        for i in range(self.n):
            temp = []
            for j in range(self.n):
                temp.append('.')
            self.current_state.append(temp)

        for block_coordinates in self.blocks:
            self.current_state[block_coordinates[0]][block_coordinates[1]] = self.BLOCK

        self.player_turn = self.X_PLAYER

    def get_console_input(self):
        valid = False
        while (not valid):
            self.n = int(input("Give a value n for the size of the board"))
            self.b = int(input("Give a value b for the amount of blocs to place on the board"))
            for i in range(self.b):
                x_str = input(f"Enter the column of the {i + 1}th  block:")
                x = self.aDict[x_str]
                y = int(input(f"Enter the row of the {i + 1}th  block:"))
                self.blocks.append((y, x))
            self.s = int(input("Give a value s for the amount of connecting positions must connect for a win"))
            self.d1 = int(input("Give a value d1 for the max depth of the algorithms for player 1"))
            self.d2 = int(input("Give a value d2 for the max depth of the algorithms for player 2"))
            self.t = int(input("Give a value t for the max time the algorithms may take for finding a move:"))
            self.p1 = int(input("Enter 2 for player 1 to be human or 3 for player 1 to be AI"))
            self.p2 = int(input("Enter 2 for player 2 to be human or 3 for player 2 to be AI"))
            self.algo1 = int(input("Enter 0 for player 1 to have minimax or enter 1 for player 1 to have alphabeta"))
            self.algo2 = int(input("Enter 0 for player 2 to have minimax or enter 1 for player 2 to have alphabeta"))
            rec = int(input("Enter 0 to have recommendations off or 1 to have recommendations on"))
            if rec == 0:
                self.recommend = False
            else:
                self.recommend = True
            self.heuristic1 = int(
                input("Enter 1 to use heuristic 1 for player 1 and enter 2 to use heuristic 2 for player 1:"))
            self.heuristic2 = int(
                input("Enter 1 to use heuristic 1 for player 2 and enter 2 to use heuristic 2 for player 2:"))
            if 3 <= self.n <= 10 and 0 <= self.b <= 2 * self.n and 3 <= self.s <= self.n:
                valid = True
            else:
                print("The given values were not valid, make sure that the following conditions are met:")
                print("n is an integer between 3 and 10 inclusive [3,...,10]")
                print("b is an integer between 0 and 2n inclusive [0,...,2n]")
                print("s is an integer between 3 and n inclusive [3,...,n]")
            print("------------------------------------------------------------------------------------------")

    def draw_board(self):
        print()
        print("  ", end="")
        for i in range(self.n):
            print(self.bDict[i], end="")
        print()
        print(" ", end="")
        print("+", end="")
        for i in range(self.n):
            print("-", end="")
        print()
        for y in range(0, self.n):
            print(f"{y}|", end="")
            for x in range(0, self.n):
                print(F'{self.current_state[y][x]}', end="")
            print()
        print()

    def draw_board_to_file(self, f):
        f.write("\n")
        f.write("  ")
        for i in range(self.n):
            f.write(self.bDict[i])
        f.write("\n")
        f.write(" ")
        f.write("+")
        for i in range(self.n):
            f.write("-")
        f.write("\n")
        for y in range(0, self.n):
            f.write(f"{y}|")
            for x in range(0, self.n):
                f.write(F'{self.current_state[y][x]}')
            f.write("\n")
        f.write("\n")

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

    def is_end(self, state):
        sub_matrices = self.get_submatrices(state)
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
                if (state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def is_sub_win(self, arr):
        items = set(arr)
        if len(items) == 1 and "." not in items and self.BLOCK not in items:
            return True, items.pop()
        return False, None

    def check_end(self, f):
        self.result = self.is_end(self.current_state)
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == self.X_PLAYER:
                print(f'The winner is {self.X_PLAYER}!')
                f.write(f'6a) The winner is {self.X_PLAYER}!\n')
                if self.heuristic1 == 1:
                    Game.heuristic1_wins += 1
                else:
                    Game.heuristic2_wins += 1
            elif self.result == self.O_PLAYER:
                print(f'The winner is {self.O_PLAYER}!')
                f.write(f'6a) The winner is {self.O_PLAYER}!\n')
                if self.heuristic2 == 1:
                    Game.heuristic1_wins += 1
                else:
                    Game.heuristic2_wins += 1
            elif self.result == '.':
                print("It's a tie!")
                f.write("6a) It's a tie!")
        return self.result

    def e2(self, state):
        start = time.time()
        possible_wins = []
        score = 0

        if self.is_end(state) == self.X_PLAYER:
            score += 1000
        elif self.is_end(state) == self.O_PLAYER:
            score -= 1000

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
            if self.O_PLAYER in lst and self.X_PLAYER not in lst and self.BLOCK not in lst:
                score -= lst.count(self.O_PLAYER)
            elif self.X_PLAYER in lst and self.O_PLAYER not in lst and self.BLOCK not in lst:
                score += lst.count(self.X_PLAYER)

        self.count_heuristic2 += 1
        end = time.time()
        self.time_heuristic2.append(round(end - start, 7))
        return score

    def e1(self, state):
        start = time.time()
        score = 0

        if self.is_end(state) == self.X_PLAYER:
            score += 1000
        elif self.is_end(state) == self.O_PLAYER:
            score -= 1000

        # row
        for row in state:
            row_score = 0
            current_element = '.'
            repeat_occurence = 0
            for element in row:
                if element == self.X_PLAYER:
                    if current_element == self.X_PLAYER:
                        repeat_occurence += 1
                        row_score += repeat_occurence
                    else:
                        current_element = self.X_PLAYER
                        repeat_occurence = 0
                        row_score += 1
                if element == self.O_PLAYER:
                    if current_element == self.O_PLAYER:
                        repeat_occurence += 1
                        row_score -= repeat_occurence
                    else:
                        current_element = self.O_PLAYER
                        repeat_occurence = 0
                        row_score -= 1
            score += row_score

        # column
        for i in range(self.n):
            col = [row[i] for row in state]
            column_score = 0
            current_element = '.'
            repeat_occurence = 0
            for element in col:
                if element == self.X_PLAYER:
                    if current_element == self.X_PLAYER:
                        repeat_occurence += 1
                        column_score += repeat_occurence
                    else:
                        current_element = self.X_PLAYER
                        repeat_occurence = 0
                        column_score += 1
                if element == self.O_PLAYER:
                    if current_element == self.O_PLAYER:
                        repeat_occurence += 1
                        column_score -= repeat_occurence
                    else:
                        current_element = self.O_PLAYER
                        repeat_occurence = 0
                        column_score -= 1
            score += column_score

        # diagonal
        valid_diagonals = self.get_valid_diags(state, self.s)
        for diagonal in valid_diagonals:
            diag_score = 0
            current_element = '.'
            repeat_occurence = 0
            for element in diagonal:
                if element == self.X_PLAYER:
                    if current_element == self.X_PLAYER:
                        repeat_occurence += 1
                        diag_score += repeat_occurence
                    else:
                        current_element = self.X_PLAYER
                        repeat_occurence = 0
                        diag_score += 1
                if element == self.O_PLAYER:
                    if current_element == self.O_PLAYER:
                        repeat_occurence += 1
                        diag_score -= repeat_occurence
                    else:
                        current_element = self.O_PLAYER
                        repeat_occurence = 0
                        diag_score -= 1
            score += diag_score

        self.count_heuristic1 += 1
        end = time.time()
        self.time_heuristic1.append(round(end - start, 7))
        return score

    def alpha_beta(self, state, depth, a, b, heuristic, maximum=False, start_time=time.time()):
        time_elapsed = round(time.time() - start_time + 0.003, 7)
        reached_time_limit = time_elapsed > self.t
        if depth <= 0 or self.is_terminal_node(state) or reached_time_limit:
            if heuristic == 1:
                v = self.e1(state)
                self.visited += 1
                self.update_depth_visits(depth)
            else:
                v = self.e2(state)
                self.visited += 1
                self.update_depth_visits(depth)
            if self.player_turn == self.X_PLAYER:
                return v, None, None, self.d1 - depth
            else:
                return v, None, None, self.d2 - depth

        possible_nodes = self.get_possible_nodes(maximum)
        depth_list = []

        if maximum:
            x = None
            y = None
            value = -10000
            for (state, row, column) in possible_nodes:
                (v, _, _, d) = self.alpha_beta(state, depth - 1, a, b, heuristic, maximum=False, start_time=start_time)
                depth_list.append(d)
                if v > value:
                    x = column
                    y = row
                    value = v
                a = max(a, value)
                if a >= b:
                    break
            return value, x, y, sum(depth_list) / len(depth_list)
        else:
            x = None
            y = None
            value = 10000
            for (state, row, column) in possible_nodes:
                (v, _, _, d) = self.alpha_beta(state, depth - 1, a, b, heuristic, maximum=True, start_time=start_time)
                depth_list.append(d)
                if v < value:
                    x = column
                    y = row
                    value = v
                b = min(a, value)
                if b <= a:
                    break
            return value, x, y, sum(depth_list) / len(depth_list)

    def update_depth_visits(self, depth):
        if self.player_turn == self.X_PLAYER:
            current_depth = self.d1 - depth
        else:
            current_depth = self.d2 - depth

        if current_depth not in self.depthVisits:
            self.depthVisits[current_depth] = 1
        else:
            self.depthVisits[current_depth] += 1

    def get_possible_nodes(self, maximum=False):
        possible_nodes = []
        if maximum:
            for row in range(self.n):
                for column in range(self.n):
                    if self.current_state[row][column] == '.':
                        self.current_state[row][column] = self.X_PLAYER
                        possible_nodes.append((self.current_state, row, column))
                        self.current_state[row][column] = '.'
        else:
            for row in range(self.n):
                for column in range(self.n):
                    if self.current_state[row][column] == '.':
                        self.current_state[row][column] = self.O_PLAYER
                        possible_nodes.append((self.current_state, row, column))
                        self.current_state[row][column] = '.'
        random.shuffle(possible_nodes)
        return possible_nodes

    def mini_max(self, state, depth, heuristic, maximum=False, start_time=time.time()):
        time_elapsed = round(time.time() - start_time + 0.003, 7)
        reached_time_limit = time_elapsed > self.t
        if depth <= 0 or self.is_terminal_node(state) or reached_time_limit:
            if heuristic == 1:
                v = self.e1(state)
                self.visited += 1
                self.update_depth_visits(depth)
            else:
                v = self.e2(state)
                self.visited += 1
                self.update_depth_visits(depth)
            if self.player_turn == self.X_PLAYER:
                return v, None, None, self.d1 - depth
            else:
                return v, None, None, self.d2 - depth

        possible_nodes = self.get_possible_nodes(maximum)
        depth_list = []
        if maximum:
            x = None
            y = None
            value = -10000
            for (state, row, column) in possible_nodes:
                (v, _, _, d) = self.mini_max(state, depth - 1, heuristic, maximum=False, start_time=start_time)
                depth_list.append(d)
                if v > value:
                    x = column
                    y = row
                    value = v
            return value, x, y, sum(depth_list) / len(depth_list)
        else:
            x = None
            y = None
            value = 10000
            for (state, row, column) in possible_nodes:
                (v, _, _, d) = self.mini_max(state, depth - 1, heuristic, maximum=True, start_time=start_time)
                depth_list.append(d)
                if v < value:
                    x = column
                    y = row
                    value = v
            return value, x, y, sum(depth_list) / len(depth_list)

    def is_terminal_node(self, state):
        full = True
        for row in state:
            if '.' in row:
                full = False

        return full

    def play(self):
        with open(f"gameTrace-{self.n}{self.b}{self.s}{self.t}.txt", "w+") as f:
            self.initial_parameters_to_file(f)
            while True:
                self.draw_board()
                if self.check_end(f):
                    self.end_of_game_metrics_to_file(f)
                    return
                start = time.time()
                if self.player_turn == self.X_PLAYER:
                    if self.algo1 == self.MINIMAX:
                        (_, x, y, average_recursive_depth) = self.mini_max(self.current_state, self.d1, self.heuristic1,
                                                                           maximum=False, start_time=start)
                    else:
                        (m, x, y, average_recursive_depth) = self.alpha_beta(self.current_state, self.d1, -1000000,
                                                                             1000000, self.heuristic1, maximum=False,
                                                                             start_time=start)
                else:
                    if self.algo2 == self.MINIMAX:
                        (_, x, y, average_recursive_depth) = self.mini_max(self.current_state, self.d2, self.heuristic2,
                                                                           maximum=True, start_time=start)
                    else:
                        (m, x, y, average_recursive_depth) = self.alpha_beta(self.current_state, self.d2, -1000000,
                                                                             1000000, self.heuristic2, maximum=True,
                                                                             start_time=start)
                end = time.time()
                self.average_recursive_depth = average_recursive_depth

                if (self.player_turn == self.X_PLAYER and self.p1 == self.HUMAN) or (
                        self.player_turn == self.O_PLAYER and self.p2 == self.HUMAN):
                    if self.recommend:
                        print(F'Evaluation time: {round(end - start, 7)}s')
                        print(F'Recommended move: x = {self.bDict[x]}, y = {y}')
                    (x, y) = self.input_move()

                    self.current_state[x][y] = self.player_turn
                    self.per_turn_metrics_to_file(end, f, start, x, y)

                if (self.player_turn == self.X_PLAYER and self.p1 == self.AI) or (
                        self.player_turn == self.O_PLAYER and self.p2 == self.AI):
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Player {self.player_turn} under AI control plays: x = {self.bDict[x]}, y = {y}')

                    self.current_state[y][x] = self.player_turn
                    self.per_turn_metrics_to_file(end, f, start, x, y)
                self.switch_player()

    def per_turn_metrics_to_file(self, end, f, start, x, y):
        if self.player_turn == self.X_PLAYER and self.heuristic1 == 1:
            self.total_moves_1 += 1
        elif self.player_turn == self.X_PLAYER and self.heuristic1 == 2:
            self.total_moves_2 += 1
        elif self.player_turn == self.O_PLAYER and self.heuristic2 == 1:
            self.total_moves_1 += 1
        elif self.player_turn == self.O_PLAYER and self.heuristic2 == 2:
            self.total_moves_2 += 1
        f.write(f"5.a) Move taken: (x,y) = ({self.bDict[x]},{y})\n")
        f.write("5.b)")
        self.draw_board_to_file(f)
        f.write(f"5.c i) The evaluation time was: {round(end - start, 7)}s \n")
        f.write(f"5.c ii) The number of states evaluated by the heuristic function is {self.visited}\n")
        self.visited = 0
        f.write(f"5 c iii) the number of nodes visited at each depth is: \n")
        numerator = 0
        denominator = 0
        for depth in self.depthVisits:
            f.write(f"Depth {depth}: {self.depthVisits[depth]}\n")

            if self.player_turn == self.X_PLAYER and self.heuristic1 == 1:
                if depth not in self.total_depth_1:
                    self.total_depth_1[depth] = self.depthVisits[depth]
                else:
                    self.total_depth_1[depth] += self.depthVisits[depth]
            elif self.player_turn == self.X_PLAYER and self.heuristic1 == 2:
                if depth not in self.total_depth_2:
                    self.total_depth_2[depth] = self.depthVisits[depth]
                else:
                    self.total_depth_2[depth] += self.depthVisits[depth]
            elif self.player_turn == self.O_PLAYER and self.heuristic2 == 1:
                if depth not in self.total_depth_1:
                    self.total_depth_1[depth] = self.depthVisits[depth]
                else:
                    self.total_depth_1[depth] += self.depthVisits[depth]
            elif self.player_turn == self.O_PLAYER and self.heuristic2 == 2:
                if depth not in self.total_depth_2:
                    self.total_depth_2[depth] = self.depthVisits[depth]
                else:
                    self.total_depth_2[depth] += self.depthVisits[depth]

            numerator += self.depthVisits[depth] * depth
            denominator += self.depthVisits[depth]
        f.write(f"5.c iv) The average depth is {numerator / denominator} \n")
        if self.player_turn == self.X_PLAYER and self.heuristic1 == 1:
            self.per_move_average_1.append(numerator / denominator)
        elif self.player_turn == self.X_PLAYER and self.heuristic1 == 2:
            self.per_move_average_2.append(numerator / denominator)
        elif self.player_turn == self.O_PLAYER and self.heuristic2 == 1:
            self.per_move_average_1.append(numerator / denominator)
        elif self.player_turn == self.O_PLAYER and self.heuristic2 == 2:
            self.per_move_average_2.append(numerator / denominator)
        self.depthVisits = {}

        f.write(f"5.c v) The average recursive depth is {self.average_recursive_depth}\n")
        if self.player_turn == self.X_PLAYER and self.heuristic1 == 1:
            self.average_recursive_depths1.append(self.average_recursive_depth)
        elif self.player_turn == self.X_PLAYER and self.heuristic1 == 2:
            self.average_recursive_depths2.append(self.average_recursive_depth)
        elif self.player_turn == self.O_PLAYER and self.heuristic2 == 1:
            self.average_recursive_depths1.append(self.average_recursive_depth)
        elif self.player_turn == self.O_PLAYER and self.heuristic2 == 2:
            self.average_recursive_depths2.append(self.average_recursive_depth)

        f.write("\n")
        self.average_recursive_depth = 0

    def end_of_game_metrics_to_file(self, f):
        if len(self.time_heuristic1) != 0:
            f.write(
                f"6b i) The average time for heuristic 1 was: {sum(self.time_heuristic1) / len(self.time_heuristic1)} \n")
            Game.scoreboard_evaluation_times.append(sum(self.time_heuristic1) / len(self.time_heuristic1))
        else:
            f.write(f"6b i) The average time for heuristic 1 was: 0 as it was not used \n")
        if len(self.time_heuristic2) != 0:
            f.write(
                f" The average time for heuristic 2 was: {sum(self.time_heuristic2) / len(self.time_heuristic2)} \n")
            Game.scoreboard_evaluation_times.append(sum(self.time_heuristic2) / len(self.time_heuristic2))
        else:
            f.write(f"The average time for heuristic 2 was: 0 as it was not used \n")

        f.write(
            f"6b ii) Heuristic 1 evaluated {self.count_heuristic1} nodes and heuristic 2 evaluated {self.count_heuristic2} nodes\n")
        Game.scoreboard_total_evaluations.append(self.count_heuristic1 + self.count_heuristic2)

        if len(self.per_move_average_1) != 0:
            f.write(
                f"6b iii) The average of the per-move average depth of the heuristic evaluation for heuristic 1 is {sum(self.per_move_average_1) / len(self.per_move_average_1)} \n")
            Game.scoreboard_depths.append(sum(self.per_move_average_1) / len(self.per_move_average_1))
        else:
            f.write(
                f"6b iii) The average of the per-move average depth of the heuristic evaluation for heuristic 1 is 0 as it was not used \n")
        if len(self.per_move_average_2) != 0:
            f.write(
                f"The average of the per-move average depth of the heuristic evaluation for heuristic 2 is {sum(self.per_move_average_2) / len(self.per_move_average_2)} \n")
            Game.scoreboard_depths.append(sum(self.per_move_average_2) / len(self.per_move_average_2))
        else:
            f.write(
                f"The average of the per-move average depth of the heuristic evaluation for heuristic 2 is 0 as it was not used \n")

        f.write("6b iv) The total number of states evaluated at each depth for heuristic 1: \n")
        for depth in self.total_depth_1:
            f.write(f"Depth {depth} : {self.total_depth_1[depth]}\n")
            if depth not in Game.scoreboard_evaluations_by_depth:
                Game.scoreboard_evaluations_by_depth[depth] = [self.total_depth_1[depth]]
            else:
                Game.scoreboard_evaluations_by_depth[depth].append(self.total_depth_1[depth])
        f.write("The total number of states evaluated at each depth for heuristic 2: \n")
        for depth in self.total_depth_2:
            f.write(f"Depth {depth} : {self.total_depth_2[depth]}\n")
            if depth not in Game.scoreboard_evaluations_by_depth:
                Game.scoreboard_evaluations_by_depth[depth] = [self.total_depth_2[depth]]
            else:
                Game.scoreboard_evaluations_by_depth[depth].append(self.total_depth_2[depth])

        f.write(
            f"6b v) The average of the per move ARD for heuristic 1 is {sum(self.average_recursive_depths1) / len(self.average_recursive_depths1)}\n")
        Game.scoreboard_recursion_depth.append(
            sum(self.average_recursive_depths1) / len(self.average_recursive_depths1))
        f.write(
            f" The average of the per move ARD for heuristic 2 is {sum(self.average_recursive_depths2) / len(self.average_recursive_depths2)}\n")
        Game.scoreboard_recursion_depth.append(
            sum(self.average_recursive_depths2) / len(self.average_recursive_depths2))

        f.write(
            f"6b vi) The total number of moves made by heuristic 1 is {self.total_moves_1} and the total number of moves made by heuristic 2 is {self.total_moves_2}\n")
        Game.scoreboard_moves_per_game.append(self.total_moves_1 + self.total_moves_2)

    def initial_parameters_to_file(self, f, board=True):
        f.write(f"1. The size n of the board is {self.n}, the number of blocks b is {self.b}, "
                f"the number of connected pieces s is {self.s} and the maximum time for evaluation t is {self.t} \n")
        f.write("2. The positions of the blocks are: \n")
        for block in self.blocks:
            f.write(f"(x,y) = ({self.bDict[block[1]]}, {block[0]})\n")
        f.write("3. Player configurations:\n")
        if self.p1 == self.HUMAN:
            f.write("Player 1 is human.\n")
        else:
            if self.algo1 == self.MINIMAX:
                f.write(
                    f"Player 1 is an AI. The maximum depth is {self.d1}. The algorithm is minimax and the heuristic used was heuristic {self.heuristic1}\n")
            else:
                f.write(
                    f"Player 1 is an AI. The maximum depth is {self.d1}. The algorithm is alphabeta and the heuristic used was heuristic {self.heuristic1}\n")
        if self.p2 == self.HUMAN:
            f.write("Player 2 is human.\n")
        else:
            if self.algo2 == self.MINIMAX:
                f.write(
                    f"Player 2 is an AI. The maximum depth is {self.d2}. The algorithm is minimax and the heuristic used was heuristic {self.heuristic2}\n")
            else:
                f.write(
                    f"Player 2 is an AI. The maximum depth is {self.d2}. The algorithm is alphabeta and the heuristic used was heuristic {self.heuristic2}\n")

        if board:
            f.write("4. The initial game board:\n")
            self.draw_board_to_file(f)

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
    s = open("scoreboard.txt", "a")

    for i in range(5):
        g = Game(n=4, b=4, s=3, t=5, d1=6, d2=6, blocks=[(0, 0), (0, 3), (3, 0), (3, 3)], h1=1, h2=2, a1=False,
                 a2=False, recommend=True)
        # g = Game(n=4, b=4, s=3, t=1, d1=6, d2=6, blocks=[(0, 0), (0, 3), (3, 0), (3, 3)], h1=1, h2=2, a1=True, a2=True, recommend=True)
        # g = Game(n=5, b=4, s=4, t=1, d1=2, d2=6, h1=1, h2=2, a1=True, a2=True, recommend=True, random_blocks=True)
        # g = Game(n=5, b=4, s=4, t=5, d1=6, d2=6, h1=1, h2=2, a1=True, a2=True, recommend=True, random_blocks=True)
        # g = Game(n=8, b=5, s=5, t=1, d1=2, d2=6, h1=1, h2=2, a1=True, a2=True, recommend=True, random_blocks=True)
        # g = Game(n=8, b=5, s=5, t=5, d1=2, d2=6, h1=1, h2=2, a1=True, a2=True, recommend=True, random_blocks=True)
        # g = Game(n=8, b=6, s=5, t=1, d1=6, d2=6, h1=1, h2=2, a1=True, a2=True, recommend=True, random_blocks=True)
        # g = Game(n=8, b=6, s=5, t=5, d1=6, d2=6, h1=1, h2=2, a1=True, a2=True, recommend=True, random_blocks=True)
        if i == 0:
            g.initial_parameters_to_file(s, board=False)

        g.play()
        print()
        print(f"PLAYED {i} GAMES\n")
        print()

    for i in range(5):
        g2 = Game(n=4, b=4, s=3, t=5, d1=6, d2=6, blocks=[(0, 0), (0, 3), (3, 0), (3, 3)], h1=2, h2=1, a1=False,
                  a2=False, recommend=True)
        # g2 = Game(n=4, b=4, s=3, t=1, d1=6, d2=6, blocks=[(0, 0), (0, 3), (3, 0), (3, 3)], h1=2, h2=1, a1=True, a2=True, recommend=True)
        # g2 = Game(n=5, b=4, s=4, t=1, d1=6, d2=2, h1=2, h2=1, a1=True, a2=True, recommend=True, random_blocks=True)
        # g2 = Game(n=5, b=4, s=4, t=5, d1=6, d2=6, h1=2, h2=1, a1=True, a2=True, recommend=True, random_blocks=True)
        # g2 = Game(n=8, b=5, s=5, t=1, d1=6, d2=2, h1=2, h2=1, a1=True, a2=True, recommend=True, random_blocks=True)
        # g2 = Game(n=8, b=5, s=5, t=5, d1=6, d2=2, h1=2, h2=1, a1=True, a2=True, recommend=True, random_blocks=True)
        # g2 = Game(n=8, b=6, s=5, t=1, d1=6, d2=6, h1=2, h2=1, a1=True, a2=True, recommend=True, random_blocks=True)
        # g2 = Game(n=8, b=6, s=5, t=5, d1=6, d2=6, h1=2, h2=1, a1=True, a2=True, recommend=True, random_blocks=True)
        g2.play()
        print()
        print(f"PLAYED {i} GAMES\n")
        print()

    s.write("\n")
    s.write("10 games \n")
    s.write("\n")

    # Print wins and win ratios for each heuristic
    s.write(f"Total wins for heuristic e1: {Game.heuristic1_wins} ({Game.heuristic1_wins / 10 * 100}%)\n")
    s.write(f"Total wins for heuristic e2: {Game.heuristic2_wins} ({Game.heuristic2_wins / 10 * 100}%)\n")
    s.write("\n")

    # Print out averaged metrics over 10 games
    times = Game.scoreboard_evaluation_times
    s.write(f"i   Average evaluation time: {sum(times) / len(times)}s\n")

    total_evaluations = Game.scoreboard_total_evaluations
    s.write(f"ii  Total heuristic evaluations: {sum(total_evaluations)}\n")
    s.write(f"    Average Total heuristic evaluations: {sum(total_evaluations) / len(total_evaluations)}\n")

    evaluations_by_depth = Game.scoreboard_evaluations_by_depth
    s.write("iii Evaluations by depth: {")
    for depth in evaluations_by_depth:
        s.write(f" {depth}:{sum(evaluations_by_depth[depth])},")
    s.write("}\n")
    s.write("    Average evaluations by depth: {")
    for depth in evaluations_by_depth:
        s.write(f" {depth}:{sum(evaluations_by_depth[depth]) / len(evaluations_by_depth[depth])},")
    s.write("}\n")

    depths = Game.scoreboard_depths
    s.write(f"iv  Average evaluation depth: {sum(depths) / len(depths)}\n")

    recursion_depth = Game.scoreboard_recursion_depth
    s.write(f"v   Average recursion depth: {sum(recursion_depth) / len(recursion_depth)}\n")

    moves = Game.scoreboard_moves_per_game
    s.write(f"vi  Average moves per game: {sum(moves) / len(moves)}\n")
    s.write("\n")


if __name__ == "__main__":
    main()
