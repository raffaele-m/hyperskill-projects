# The script take the folder name as argument and scrape the webpage passed as input.

import os
import re
import argparse
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def check_dir(directory):
    if not os.path.exists(f'{directory}'):
        os.mkdir(f'{directory}')
    else:
        pass


def check_domain(directory):
    url = input()
    domain = url
    file_path = os.path.join(directory, domain)
    if url == 'exit':
        exit()
    elif url == 'back':
        if len(history) >= 2:
            _ = history.pop()
            back = history.pop()
            with open(f'{back}', 'r') as f:
                print('\n'.join(f.readlines()))
    elif '.' not in url:
        text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        if url+'.txt' in text_files:
            with open(f'{file_path}', 'r') as f:
                print('\n'.join(f.readlines()))
        else:
            print('Error: Incorrect URL')
    elif '.' in url:
        url = 'https://'+url if 'https://' not in url else url
        m = re.search(r'((https?)://)?(\w+\.)*(?P<domain>\w+.?)\.(\w+)(/.*)?', url)
        domain = m.group('domain')
        file_path = os.path.join(directory, domain)
        try:
            r = requests.get(url)
            if r:
                soup = BeautifulSoup(r.content, 'html.parser')
                tag_list = soup.find_all(['p', 'a', 'ul', ' ol', 'li'])
                t = tag_list[0].get_text()
                testo = [tag.get_text(strip=True) for tag in tag_list]
                for line in testo:
                    print(Fore.BLUE + line)
                with open(f'{file_path}', 'w') as f:
                    f.write('\n'.join(testo))
                history.append(file_path)
            else:
                print('Error: Incorrect URL')
        except requests.exceptions.ConnectionError:
            print('Error: Incorrect URL')
    else:
        print('Error: Incorrect URL')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_input")
    args = parser.parse_args()
    directory_input = args.dir_input
    check_dir(directory_input)
    history = deque()
    while True:
        check_domain(args.dir_input)
