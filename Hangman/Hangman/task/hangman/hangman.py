# Write your code here
import random
import re


def not_lower_ascii(word_check):
    exp = re.compile('[a-z]')
    if re.match(exp, word_check):
        return False
    else:
        return True


def first_choice():
    while True:
        choice = input('Type "play" to play the game, "exit" to quit:')
        if choice == 'play':
            return True
        elif choice == 'exit':
            exit(0)


print('H A N G M A N')
first_choice()
dictionary = ['python', 'java', 'kotlin', 'javascript']
word = dictionary[random.randint(0, len(dictionary)-1)]
available_try = 8
hidden_word = '-'*len(word)
hidden_list = list(hidden_word)
guessed_char = list()

while available_try != 0:
    print('\n'+''.join(hidden_list))
    guess = input('Input a letter: ')
    if len(guess) != 1:
        print('You should input a single letter')
    elif not_lower_ascii(guess):
        print('It is not an ASCII lowercase letter')
    elif guess in guessed_char:
        print('You already typed this letter')
    elif guess not in word:
        print('No such letter in the word')
        available_try -= 1
    else:
        for n, letter in enumerate(word):
            if guess == letter:
                hidden_list[n] = letter
    if '-' not in hidden_list:
        print('\n'+word)
        print('You guessed the word!')
        print('You survived!')
        exit(0)
    guessed_char.append(guess)
print('You are hanged!')
