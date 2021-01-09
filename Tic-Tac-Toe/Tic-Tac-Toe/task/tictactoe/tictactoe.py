# write your code here
class TicTacToe:
    
    WINS_COMB = {
        1: '123',
        2: '456',
        3: '789',
        4: '147',
        5: '258',
        6: '369',
        7: '159',
        8: '357'
    }
    
    def __init__(self):
        self.dash_boundary = '---------'
        self.sequence, self.grid = '         ', None
        self.player = 'X'
        self.array_to_matrix()
        self.print_result()
        while True:
            self.check_coordinates()
            result = self.analyze()
            self.print_result(result)

    @staticmethod
    def represent_int(x):
        try:
            int(x)
            return True
        except TypeError:
            return False

    def check_coordinates(self):
        x, y = input('Enter the coordinates: ').split(' ')
        try:
            assert self.represent_int(x) and self.represent_int(y), "You should enter numbers!"
            x, y = int(x), int(y)
            assert 1 <= x <= 3 and 1 <= y <= 3, "Coordinates should be from 1 to 3!"
        except AssertionError as e:
            print(e)
            return self.check_coordinates()
        if self.grid[x - 1][y - 1] != ' ':
            print('This cell is occupied! Choose another one!')
            return self.check_coordinates()
        else:
            self.grid[x - 1][y - 1] = self.player
            self.sequence = ''.join([el for group in self.grid for el in group])
            if self.player == 'X':
                self.player = 'O'
            else:
                self.player = 'X'
            return

    def array_to_matrix(self):
        self.grid = []
        if len(self.sequence) == 9:
            for i in range(0, 9, 3):
                self.grid.append([*self.sequence[i:i+3]])
        else:
            print('Error not enough values')
        
    def analyze(self):
        if self.impossible():
            return 'Impossible'
        elif self.check_wins('X'):
            return 'X wins'
        elif self.check_wins('O'):
            return 'O wins'
        elif self.game_not_finished():
            return 'Game not finished'
        elif self.draw():
            return 'Draw'
        else:
            return False

    def game_not_finished(self):
        return True if '_' in self.sequence else False
    
    def draw(self):
        return 'Draw' if '_' not in self.sequence and ' ' not in self.sequence else False

    def print_result(self, output=False):
        print(self.dash_boundary)
        for line in self.grid:
            print('| ' + ' '.join(line) + ' |')
        print(self.dash_boundary)
        if output:
            print(output)
            exit()

    def check_wins(self, char):
        if char != ' ' and char != '_':
            for pos in self.WINS_COMB.values():
                if self.sequence[int(pos[0]) - 1] == self.sequence[int(pos[1]) - 1] == self.sequence[int(pos[2]) - 1] == char:
                    return True
        return False

    def impossible(self):
        if abs(self.sequence.count('X') - self.sequence.count('O')) > 1:
            return True
        elif self.check_wins('X') and self.check_wins('O'):
            return True
        else:
            return False


if __name__ == '__main__':
    TicTacToe()
