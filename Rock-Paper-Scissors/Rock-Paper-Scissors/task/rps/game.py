# Write your code here
import random


class RockPaperScissors:
    C_LIST = ['rock', 'fire', 'scissors', 'snake', 'human',
              'tree', 'wolf', 'sponge', 'paper', 'air',
              'water', 'dragon', 'devil', 'lightning', 'gun']

    def __init__(self):
        self.choice, self.name, self.defined_set = None, None, None
        self.score = 0
        self.score_name()

    def define_list(self):
        self.defined_set = set(input().lower().split(','))
        if self.defined_set == {''}:
            self.defined_set = {'rock', 'paper', 'scissors'}
            return self.choose()
        elif self.defined_set.intersection(set(self.C_LIST)) == self.defined_set:
            print("Okay, let's start")
            return self.choose()
        else:
            print('Invalid Input')
            self.define_list()

    def score_name(self):
        self.name = input('Enter your name: ')
        print('Hello, {}'.format(self.name))
        with open('rating.txt', 'r') as f:
            for line in f:
                if line.split()[0] == self.name:
                    self.score = int(line.split()[1])
        return self.define_list()

    def choose(self):
        self.choice = input()
        if self.choice == '!exit':
            exit('Bye!')
        elif self.choice == '!rating':
            print(f'Your rating: {self.score}')
            return self.choose()
        elif self.choice in self.defined_set:
            return self.play()
        else:
            print('Invalid input')
            return self.choose()

    def check(self):
        c_player = self.choice
        c_com = random.choice(list(self.defined_set))
        win_lose_list = self.C_LIST[self.C_LIST.index(c_player)+1:]
        win_lose_list.extend(self.C_LIST[:self.C_LIST.index(c_player)])
        n_half = int((len(win_lose_list) / 2))
        try:
            if c_player == c_com:
                self.score += 50
                print(f'There is a draw ({c_player})')
            elif c_com in win_lose_list[:n_half]:
                self.score += 100
                print(f'Well done. The computer chose {c_com} and failed')
            else:
                print(f'Sorry, but the computer chose {c_com}')
        except (KeyError, ValueError):
            print('Invalid input')
            self.choose()

    def play(self):
        self.check()
        return self.choose()


RockPaperScissors()
