import collections
import random
import re


def get_tokens(file, statistics=False):
    tok = file.read().split()
    if statistics:
        print('Corpus statistics.')
        print(f'All tokens: {len(tok)}')
        print(f'Unique tokens: {len(set(tok))}\n')
    return tok


def get_trigrams(tokens_list):
    res = []
    for i in range(len(tokens_list) - 2):
        res.append([' '.join(tokens_list[i:i+2]), tokens_list[i+2]])
    return res


def get_frequencies(gram_list):
    res = collections.defaultdict(collections.Counter)
    for head, tail in gram_list:
        res[head][tail] += 1
    return res


def generate_sentence(freq):
    sentence_list = []
    while True:
        if len(sentence_list) == 0:
            r_capword = re.compile(r'^[A-Z][^.?!]*$')
            next_word = random.choice(list(filter(lambda x: r_capword.match(x), freq.keys())))
            sentence_list = [*next_word.split()]
        elif len(sentence_list) >= 5:
            try:
                r_capword = re.compile(r'.*[.?!]$')
                choice = random.choice(list(filter(lambda x: r_capword.match(x[0]), freq[next_word].items())))
                sentence_list.append(choice[0])
                return ' '.join(sentence_list)
            except IndexError:
                r_capword = re.compile(r'.*[^.?!]$')
                r_list = dict(filter(lambda x: r_capword.match(x[0]), freq[next_word].items()))
                if r_list == {}:
                    sentence_list = []
                    continue
                choice = random.choices(list(r_list.keys()), list(r_list.values()))[0]
                sentence_list.append(choice)
                next_word = ' '.join(sentence_list[-2:])
        else:
            r_capword = re.compile(r'.*[^.?!]$')
            r_list = dict(filter(lambda x: r_capword.match(x[0]), freq[next_word].items()))
            if r_list == {}:
                sentence_list = []
                continue
            choice = random.choices(list(r_list.keys()), list(r_list.values()))[0]
            sentence_list.append(choice)
            next_word = ' '.join(sentence_list[-2:])

with open(f'{input()}', encoding='utf-8', mode='r') as f:
    tokens = get_tokens(f)
    trigrams = get_trigrams(tokens)
    frequencies = get_frequencies(trigrams)
    for _ in range(10):
        sentence = generate_sentence(frequencies)
        print(sentence)
