# Write your code here
import json
import random
import argparse
from operator import itemgetter
from io import StringIO


def menu():
    available_options = {
        'add': add_card,
        'remove': remove_card,
        'import': import_card,
        'export': export_card,
        'ask': ask_card,
        'exit': exit_program,
        'log': log,
        'hardest card': hardest_card,
        'reset stats': reset_stats
    }
    welcome_message = 'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):'
    print_and_log(welcome_message)
    choice = input()
    memory_file.write(choice+'\n')
    if choice not in available_options.keys():
        print('Try again')
        menu()
    else:
        result = available_options[choice]()
        print_and_log(result)
        menu()


def add_card():
    while True:
        print_and_log('The card:')
        term = input()
        memory_file.write(term+'\n')
        if term in cards_deck.keys():
            print_and_log(f'The card "{term}" already exists.')
        else:
            break
    while True:
        definition = input('The definition of the card:')
        if any(definition in v['definition'] for v in cards_deck.values()):
            print(f'The definition "{definition}" already exists.')
        else:
            break
    cards_deck[term] = {'definition': definition, 'n_errors': 0}
    return f'The pair ("{term}","{definition}") has been added.'


def remove_card():
    del_term = input('Which card?')
    try:
        cards_deck.pop(del_term)
        return 'The card has been removed.'
    except KeyError:
        return f'Can\'t remove "{del_term}": there is no such card.'


def import_card(filename=None):
    if filename is None:
        print_and_log('File name:')
        file_name = input()
    else:
        file_name = filename
    try:
        with open(file_name, 'r') as file:
            cards_loaded = json.load(file)
            cards_deck.update(cards_loaded)
        return f'{str(len(cards_loaded))} cards have been loaded.'
    except IOError:
        return 'File not found.'


def export_card(filename=None):
    if filename is None:
        print_and_log('File name:')
        file_name = input()
    else:
        file_name = filename
    with open(file_name, 'w') as file:
        json.dump(cards_deck, file)
    return f'{str(len(cards_deck))} cards have been saved.'


def ask_card():
    print_and_log('How many times to ask?')
    n_cards = int(input())
    try:
        for i in range(n_cards):
            rand_term = random.choice(list(cards_deck.keys()))
            print_and_log(f'Print the definition of "{rand_term}":')
            ans_def = input()
            if ans_def == cards_deck[rand_term]['definition']:
                print_and_log('Correct!')
            elif any(ans_def in v['definition'] for v in cards_deck.values()):
                for k, v in cards_deck.items():
                    if v['definition'] == ans_def:
                        message = f'Wrong. The right answer is "{cards_deck[rand_term]["definition"]}", but your definition is correct for "{k}".'
                        print_and_log(message)
                try:
                    cards_deck[rand_term]['n_errors'] += 1
                except KeyError:
                    cards_deck[rand_term]['n_errors'] = 0
            else:
                print_and_log(f'Wrong. The right answer is "{cards_deck[rand_term]["definition"]}"')
                try:
                    cards_deck[rand_term]['n_errors'] += 1
                except KeyError:
                    cards_deck[rand_term]['n_errors'] = 0
    except IndexError:
        print_and_log('No card added.')
    return None


def exit_program():
    if args.export_to is not None:
        print(export_card(filename=args.export_to))
    print_and_log('Bye bye!')
    memory_file.close()
    exit()


def log():
    memory_file.seek(0)
    print_and_log('File name:')
    file_name = input()
    with open(file_name, 'w') as file:
        file.write(memory_file.getvalue())
    return 'The log has been saved.'


def hardest_card():
    dict_hardest = {k: v['n_errors'] for k, v in cards_deck.items() if v['n_errors'] == max(cards_deck.values(),
                    key=itemgetter('n_errors'))['n_errors'] and v['n_errors'] != 0}
    if not dict_hardest:
        print_and_log('The are no cards with errors.')
    elif len(dict_hardest) == 1:
        return f'The hardest card is "{list(dict_hardest.keys())[0]}". You have {list(dict_hardest.values())[0]} errors answering it.'
    else:
        return f"The hardest cards are {', '.join(list(dict_hardest.keys()))}."


def reset_stats():
    for k in cards_deck.keys():
        cards_deck[k]['n_errors'] = 0
    return 'Card statistics have been reset.'


def print_and_log(string):
    if string is not None:
        memory_file.write(string+'\n')
        print(string)


def parsing_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from', type=str)
    parser.add_argument('--export_to', type=str)
    global args
    args = parser.parse_args()
    if args.import_from is not None:
        print_and_log(import_card(filename=args.import_from))


if __name__ == "__main__":
    cards_deck = {}
    memory_file = StringIO()
    parsing_args()
    menu()
