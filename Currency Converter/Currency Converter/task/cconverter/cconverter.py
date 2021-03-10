# write your code here!
import requests
import json

code_in = input().lower()
eur_url = 'http://www.floatrates.com/daily/eur.json'
r = requests.get(eur_url)
dict_rates = json.loads(r.text)
analyzed = {'eur': dict_rates}
usd_url = 'http://www.floatrates.com/daily/usd.json'
r = requests.get(usd_url)
dict_rates = json.loads(r.text)
analyzed['usd'] = dict_rates


while set(analyzed.keys()) != set(dict_rates.keys()):
    code_out = input().lower()
    if code_out.strip() == '':
        exit()
    amount = float(input())
    print('Checking the cache...')
    if code_out in analyzed.keys():
        print('Oh! It is in the cache!')
        rate = analyzed[code_out][code_in]['rate']
        print(f'You received {amount / rate} {code_out.upper()}.')
    else:
        print('Sorry, but it is not in the cache!')
        url_rates = f'http://www.floatrates.com/daily/{code_out}.json'
        r = requests.get(url_rates)
        dict_rates = json.loads(r.text)
        analyzed[code_out] = dict_rates
        rate = dict_rates[code_in]['rate']
        print(f'You received {amount / rate} {code_out.upper()}.')
