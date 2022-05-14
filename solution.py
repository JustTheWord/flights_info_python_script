import csv
import argparse
from typing import *
from sys import stdin
from control_ticket import control_ticket, layover_time
# python -m solution data.csv BTW REJ --bags=1

# ------------- Global variables -------------
# a dictionary for mapping "origin" to list with all possible "destinations"
directs: Dict[str, List] = dict()
# set with the all feasible routes to sort them by price
create_route = list()
feasible_routes = list()
# --------------------------------------------


def searching_route(name: str,
                    index: int,
                    ticket_info,
                    arrival: float) -> None:

    if name == dest:
        _list = create_route.copy()
        feasible_routes.append(_list)

    elif name in {ticket[2]['origin'] for ticket in create_route}:  # senseless routes like a -> b -> a (repeated) -> d
        return

    else:
        for next_airport in directs[name]:

            if next_airport[0] < index:             # the ticket date is earlier than our flight
                continue

            layover_t = layover_time(arrival, next_airport[2]['departure'])
            if layover_t > 6 or layover_t < 1:      # the layover time is less than an hour or more than six hours
                continue

            if args.bags > int(ticket_info['bags_allowed']):  # there is not enough number of allowed bags for the trip
                continue

            create_route.append(next_airport)
            index, ticket_info, air_name, arrival = next_airport[0], next_airport[2], next_airport[2]["destination"], next_airport[2]["arrival"]
            searching_route(air_name, index, ticket_info, arrival)
            create_route.pop()
    return


parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default='example/example3.csv')
# parser.add_argument('origin', nargs=1, type=str, help='Origin airport of the trip')
# parser.add_argument('dest', nargs=1, type=str, help='The final destination of the trip')
parser.add_argument('--bags', type=int, default=0, help='Number of requested bags')
parser.add_argument('--ret', action='store_true', help='Is it a return flight?')
args = parser.parse_args()
# ------- Arguments -------
# origin: str = args.origin[0]
origin = 'WTN'
# dest: str = args.dest[0]
dest = 'ZRW'
# --------------------- Reading from file ---------------------
with args.infile as file:
    reader = csv.DictReader(file)
    for i, route in enumerate(reader):
        if route['origin'] in directs:
            directs[route['origin']].append((i, route['origin'], route))
        else:
            directs[route['origin']] = [(i, route['origin'], route)]
# -------------------------------------------------------------
if origin not in directs:
    print("Sorry, there's no such origin airport in the list")
    exit(0)
else:
    for ticket in directs[origin]:
        create_route.append(ticket)
        index, ticket_info, air_name, arrival = ticket[0], ticket[2], ticket[2]["destination"], ticket[2]["arrival"]
        searching_route(air_name, index, ticket_info, arrival)
        create_route.pop()
# --------- all possible routes ---------
# for elem in feasible_routes[0]:
#     print(elem)
for route in feasible_routes:
    print('-----------------------------')
    for ticket in route:
        print(ticket)
