# write your code here
import random
import copy

class TicTacToe:

    DASH_BOUNDARY = '---------'

    def __init__(self):
        self.grid = [[' ', ' ', ' '],
                     [' ', ' ', ' '],
                     [' ', ' ', ' ']]
        self.current_player = 'X'
        self.menu()

    @staticmethod
    def represent_int(x):
        try:
            int(x)
            return True
        except TypeError:
            return False

    def menu(self):
        options = {'start', 'easy', 'medium', 'hard', 'user', 'exit'}
        choice = input('Input command: ').split(' ')
        if choice[0] == 'exit':
            return self.exit()
        try:
            assert len(choice) == 3
            assert choice[0] in ['start', 'exit']
            assert all(el in options for el in choice[1:])
        except AssertionError:
            print('Bad parameters!')
            return self.menu()
        self.print_result()
        while True:
            if self.current_player == 'X':
                self.user_play() if choice[1] == 'user' else self.cpu_game(choice[1])
            else:
                self.user_play() if choice[2] == 'user' else self.cpu_game(choice[2])
            result = self.analyze()
            self.print_result(result)

    @staticmethod
    def empty_slots(grid):
        return [(x, y) for x, row in enumerate(grid) for y, el in enumerate(row) if el == ' ']

    def user_play(self):
        try:
            coordinates = input('Enter the coordinates: ').split(' ')
            if len(coordinates) != 2 or coordinates == ['']:
                raise AssertionError('You should enter numbers!')
            x, y = coordinates[0], coordinates[1]
            assert self.represent_int(x) and self.represent_int(y), "You should enter numbers!"
            x, y = int(x) - 1, int(y) - 1
            assert 0 <= x <= 2 and 0 <= y <= 2, "Coordinates should be from 1 to 3!"
        except AssertionError as e:
            print(e)
            return self.user_play()
        except ValueError:
            print("You should enter numbers!")
            return self.user_play()
        if self.grid[x][y] != ' ':
            print('This cell is occupied! Choose another one!')
            return self.user_play()
        else:
            self.grid[x][y] = self.current_player
            self.current_player = self.switch_player()
            return

    def switch_player(self):
        return {'X': 'O', 'O': 'X'}[self.current_player]

    def cpu_game(self, difficulty):
        if difficulty == 'easy':
            return self.cpu_easy()
        elif difficulty == 'medium':
            return self.cpu_medium()
        elif difficulty == 'hard':
            return self.cpu_hard()
        else:
            return

    def cpu_easy(self, message=True):
        print('Making move level "easy"') if message else None
        available_choice = self.empty_slots(self.grid)
        x, y = random.choice(available_choice)
        self.grid[x][y] = self.current_player
        self.current_player = self.switch_player()
        return

    def cpu_medium(self):
        print('Making move level "medium"')
        available_spots = self.empty_slots(self.grid)
        temp_grid = copy.deepcopy(self.grid)
        for coords in available_spots:
            for move in ['X', 'O']:
                x, y = coords
                temp_grid[x][y] = move
                if self.check_wins(temp_grid, move):
                    self.grid[x][y] = self.current_player
                    self.current_player = self.switch_player()
                    del temp_grid
                    return
                else:
                    temp_grid[x][y] = ' '
        del temp_grid
        x, y = random.choice(available_spots)
        self.grid[x][y] = self.current_player
        self.current_player = self.switch_player()

    def cpu_hard(self):
        grid = copy.deepcopy(self.grid)
        best_score = -100000
        best_move = None
        player = self.current_player
        human = False
        available_spots = self.empty_slots(grid)
        if len(available_spots) == 9:
            return self.cpu_easy(message=False)
        for i, coords in enumerate(available_spots):
            x, y = coords
            grid[x][y] = player
            new_player = {'X': 'O', 'O': 'X'}[player]
            score = self.min_max(grid, new_player, not human)
            grid[x][y] = ' '
            if score > best_score:
                best_score = score
                best_move = coords
        x, y = best_move
        self.grid[x][y] = self.current_player
        self.current_player = self.switch_player()

    def min_max(self, grid, player, human=False):
        scores = []
        new_grid = copy.deepcopy(grid)
        available_spots = self.empty_slots(new_grid)
        if self.check_wins(new_grid, {'X': 'O', 'O': 'X'}[self.current_player]):
            return -1
        elif self.check_wins(new_grid, self.current_player):
            return 1
        elif self.draw(new_grid):
            return 0
        for coords in available_spots:
            x, y = coords
            new_grid[x][y] = player
            new_player = {'X': 'O', 'O': 'X'}[player]
            result = self.min_max(new_grid, new_player, not human)
            scores.append(result)
            new_grid[x][y] = ' '
        if human:
            return min(scores)
        else:
            return max(scores)

    def analyze(self):
        if self.check_wins(self.grid, 'X'):
            return 'X wins'
        elif self.check_wins(self.grid, 'O'):
            return 'O wins'
        elif self.draw(self.grid):
            return 'Draw'
        else:
            return False

    def draw(self, grid):
        return len(self.empty_slots(grid)) == 0

    def print_result(self, output=False):
        print(self.DASH_BOUNDARY)
        for line in self.grid:
            print('| ' + ' '.join(line) + ' |')
        print(self.DASH_BOUNDARY)
        if output:
            print(output)
            self.__init__()

    @staticmethod
    def check_wins(board, char):
        grid = board
        if char != ' ' and char != '_':
            if [grid[0][0], grid[1][1], grid[2][2]].count(char) == 3 or \
                    [grid[0][2], grid[1][1], grid[2][0]].count(char) == 3:
                return True
            for i in range(3):
                if grid[i].count(char) == 3 or [grid[0][i], grid[1][i], grid[2][i]].count(char) == 3:
                    return True
        return False

    @staticmethod
    def match_point(board, char):
        grid = board
        if [grid[0][0], grid[1][1], grid[2][2]].count(char) == 2:
            return [(i, i) for i in range(3) if grid[i][i] == ' ']

    @staticmethod
    def exit():
        exit()


if __name__ == '__main__':
    TicTacToe()
