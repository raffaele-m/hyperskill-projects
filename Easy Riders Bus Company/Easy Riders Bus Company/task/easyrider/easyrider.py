# Write your awesome code here
import json
import re
from collections import Counter
from datetime import datetime


def compare_type(value, type_to_compare, required=True):
    if not value and not required:
        return True
    if not value and type_to_compare is not int:
        return False
    elif type_to_compare == 'Char':
        return value in "OSF" or value == ''
    elif type_to_compare == 'HH:MM' and re.match('^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', value):
        return True
    else:
        return type(value) == type_to_compare


def check_lines(ride_list):
    bus_id_list = []
    for ride in ride_list:
        bus_id_list.append(ride['bus_id'])
    return dict(Counter(bus_id_list))


def check_stop_type(ride_list):
    dict_stop_type_list = {'start': [], 'transfer': [], 'stop': []}
    accepted_transfer_stop = ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
    for ride in ride_list:
        try:
            if ride.get('stop_name') in accepted_transfer_stop:
                dict_stop_type_list['transfer'].append(ride.get('stop_name'))
            if ride.get('stop_type') == 'S':
                dict_stop_type_list['start'].append(ride['stop_name'])
            elif ride.get('stop_type') == 'F':
                dict_stop_type_list['stop'].append(ride['stop_name'])
                if ride.get('stop_name') in accepted_transfer_stop:
                    dict_stop_type_list['transfer'].append(ride.get('stop_name'))
        except KeyError:
            print('key not present')
    stop_type_counter = {key: len(set(value)) for key, value in dict_stop_type_list.items()}
    # print(f'Start stops: {stop_type_counter["start"]} {sorted(list(set(dict_stop_type_list["start"])))}')
    # print(f'Transfer stops: {stop_type_counter["transfer"]} {sorted(list(set(dict_stop_type_list["transfer"])))}')
    # print(f'Finish stops: {stop_type_counter["stop"]} {sorted(list(set(dict_stop_type_list["stop"])))}')


def check_line_stop(ride_list):
    dict_lines = {}
    dict_stop_type_list = {'start': {'names': [], 'counter': 0},
                           'transfer': {'names': [], 'counter': 0},
                           'stop': {'names': [], 'counter': 0}}
    accepted_transfer_stop = ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
    for n, doc in enumerate(ride_list):
        if doc['bus_id'] not in dict_lines:
            dict_lines[doc['bus_id']] = {'routes': [], 'start': False, 'stop': False}
        dict_lines[doc['bus_id']]['routes'].append(doc)
        if doc['stop_name'] in accepted_transfer_stop:
            dict_stop_type_list['transfer']['names'].append(doc.get('stop_name'))
        if doc['stop_type'] == 'S':
            dict_lines[doc['bus_id']]['start'] = True
            dict_stop_type_list['start']['names'].append(doc.get('stop_name'))
        elif doc['stop_type'] == 'F':
            dict_lines[doc['bus_id']]['stop'] = True
            dict_stop_type_list['stop']['names'].append(doc.get('stop_name'))
        for route in dict_stop_type_list.values():
            route['names'] = sorted(list(set(route['names'])))
            route['counter'] = len(route['names'])
    for key, value in dict_lines.items():
        if not value['start'] or not value['stop']:
            return print(f'There is no start or end stop for the line: {key}.')
    for stop_type, stop_info in dict_stop_type_list.items():
        print(f"{str(stop_type).title()} stops: {stop_info['counter']} {stop_info['names']}")


def arrival_time_check(ride_list):
    dict_lines = {}
    cnt = 0
    for n, doc in enumerate(ride_list):
        if doc['bus_id'] not in dict_lines:
            dict_lines[doc['bus_id']] = {}
            dict_lines[doc['bus_id']]['time'] = doc['a_time']
            dict_lines[doc['bus_id']]['time_error'] = False
        else:
            if datetime.strptime(doc['a_time'], '%H:%M') < datetime.strptime(dict_lines[doc['bus_id']]['time'], '%H:%M')\
                    and not dict_lines[doc['bus_id']]['time_error']:
                dict_lines[doc['bus_id']]['station'] = doc['stop_name']
                dict_lines[doc['bus_id']]['time'] = doc['a_time']
                dict_lines[doc['bus_id']]['time_error'] = True
                cnt += 1
            else:
                dict_lines[doc['bus_id']]['time'] = doc['a_time']
    if cnt == 0:
        print('Arrival time test:\nOK')
    else:
        for route, time_station in dict_lines.items():
            if time_station.get('station', False):
                print(f"bus_id line {route}: wrong time on station {time_station['station']}")


def check_on_demand_stops(ride_list):
    accepted_on_demand = ['Fifth Avenue']
    wrong_stop = []
    for doc in ride_list:
        if doc['stop_name'] not in accepted_on_demand and doc['stop_type'] == 'O':
            wrong_stop.append(doc['stop_name'])
    if wrong_stop:
        print('On demand stops test:')
        print(f'Wrong stop type {sorted(wrong_stop)}')
    else:
        print('On demand stops test:\nOK')
    return None


report = {
     "bus_id": 0,
     "stop_id": 0,
     "stop_name": 0,
     "next_stop": 0,
     "stop_type": 0,
     "a_time": 0
}

values_types = {
     "bus_id": {"type": int, "required": True},
     "stop_id": {"type": int, "required": True},
     "stop_name": {"type": str, "required": True},
     "next_stop": {"type": int, "required": True},
     "stop_type": {"type": 'Char', "required": False},
     "a_time": {"type": "HH:MM", "required": True}
}

inp_list_dict = json.loads(input())
err_counter = 0
pattern = r'^[A-Z].*(Road|Avenue|Boulevard|Street)$'

# input example
# [
#     {
#         "bus_id": 128,
#         "stop_id": 1,
#         "stop_name": "Prospekt Avenue",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": "08:12"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 3,
#         "stop_name": "Elm Street",
#         "next_stop": 5,
#         "stop_type": "",
#         "a_time": "08:19"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 5,
#         "stop_name": "Fifth Avenue",
#         "next_stop": 7,
#         "stop_type": "O",
#         "a_time": "08:25"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 7,
#         "stop_name": "Sesame Street",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:37"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 2,
#         "stop_name": "Pilotow Street",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": "09:20"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 3,
#         "stop_name": "Elm Street",
#         "next_stop": 6,
#         "stop_type": "",
#         "a_time": "09:45"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 7,
#         "stop_type": "",
#         "a_time": "09:59"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 7,
#         "stop_name": "Sesame Street",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "10:12"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 4,
#         "stop_name": "Bourbon Street",
#         "next_stop": 6,
#         "stop_type": "S",
#         "a_time": "08:13"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:16"
#     }
# ]


for inp_dict in inp_list_dict:
    for k, v in report.items():
        if not compare_type(inp_dict.get(k), values_types.get(k)['type'], values_types.get(k)['required']):
            report[k] += 1
            err_counter += 1
        if k == 'stop_name' and not re.match(pattern, inp_dict.get(k)):
            report[k] += 1
            err_counter += 1

compare_type(inp_list_dict, values_types)
check_lines(inp_list_dict)
check_stop_type(inp_list_dict)
check_line_stop(inp_list_dict)
arrival_time_check(inp_list_dict)
check_on_demand_stops(inp_list_dict)

