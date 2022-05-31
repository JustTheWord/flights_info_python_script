import csv
import json
import argparse
from typing import *
from make_json import make_json_like_list
from control_ticket import bags_check_ok, layover_time

# ------------- Global variables -------------
# a dictionary for mapping "origin" to list with all possible "destinations"
directs: Dict[str, List] = dict()
# list with the tickets to make a trip
create_trip = list()
# list with the all feasible routes
feasible_routes = list()
# --------------------------------------------


def searching_route(name: str,
                    index: int,
                    ticket_info,
                    arrival: float) -> None:

    if name == dest:
        if bags_check_ok(args.bags, int(ticket_info['bags_allowed'])):
            feasible_routes.append(create_trip.copy())

    elif name in {ticket[2]['origin'] for ticket in create_trip}:  # senseless routes like a -> b -> a (repeated) -> d
        return

    else:
        for next_airport in directs[name]:

            if next_airport[0] < index:             # the ticket date is earlier than our flight
                continue

            layover_t = layover_time(arrival, next_airport[2]['departure'])
            if layover_t > 6 or layover_t < 1:      # the layover time is less than an hour or more than six hours
                continue

            if not bags_check_ok(args.bags,
                                 int(next_airport[2]['bags_allowed'])):  # there is not enough number of allowed bags
                continue

            create_trip.append(next_airport)
            index, ticket, air_name, layover_check = next_airport[0], next_airport[2], next_airport[2]["destination"], next_airport[2]["arrival"]
            searching_route(air_name, index, ticket, layover_check)
            create_trip.pop()
    return


parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), help='The data set which we work with')
parser.add_argument('origin', nargs=1, type=str, help='Origin airport of the trip')
parser.add_argument('dest', nargs=1, type=str, help='The final destination of the trip')
parser.add_argument('--bags', type=int, default=0, help='Number of requested bags')
parser.add_argument('--ret', action='store_true', help='Is it a return flight?')
args = parser.parse_args()
# ------- Arguments -------
origin: str = args.origin[0]
dest: str = args.dest[0]
# --------------------- Reading from file ---------------------
with args.file as file:
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
        create_trip.append(ticket)
        index, ticket_info, air_name, arrival = ticket[0], ticket[2], ticket[2]["destination"], ticket[2]["arrival"]
        searching_route(air_name, index, ticket_info, arrival)
        create_trip.pop()

# --------- all possible routes ---------
_list = make_json_like_list(feasible_routes, args.bags)
# ------ sort trips by total price ------
_list.sort(key=lambda x: x["total_price"])
print(json.dumps(_list, indent=4))
