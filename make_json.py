from typing import List, Dict
from datetime import datetime


def travel_time(depart_time, arrival_time):
    # the arrival date partitioned to the date and the precise time
    date, _, time = depart_time.rpartition('T')
    year, month, day = map(lambda s: int(s), date.split('-'))
    hours, minutes, seconds = map(lambda s: int(s), time.split(':'))
    depart_time = datetime(year, month, day, hours, minutes, seconds)
    # the departure date partitioned to the date and the precise time
    date, _, time = arrival_time.rpartition('T')
    year, month, day = map(lambda s: int(s), date.split('-'))
    hours, minutes, seconds = map(lambda s: int(s), time.split(':'))
    arrival_time = datetime(year, month, day, hours, minutes, seconds)
    # finding the total time of the layover in hours
    return arrival_time - depart_time


def make_json_like_list(all_trips: List,
                        searched_bags: int) -> List:
    json_list: List[Dict] = list()  # a list to convert to a json structure

    # -- Go through the trips in the list of all possible trips --
    for trip in all_trips:
        total = 0               # a variable for counting the whole price of a trip
        bag_min = 1000          # a variable for number of allowed bags
        all_tickets = list()    # a list for route (sequence of tickets)
        one_trip = dict()       # a dictionary for a trip

        # -- Go through the tickets in a trip --
        for ticket in trip:

            all_tickets.append(ticket[2])
            total += float(ticket[2]['base_price']) + float(ticket[2]['bag_price'])

            if bag_min > int(ticket[2]['bags_allowed']):
                bag_min = int(ticket[2]['bags_allowed'])

        last_ticket = trip[-1][2]
        first_ticket = trip[0][2]

        # -- Fill the dictionary with the trip info --
        one_trip["flights"] = all_tickets
        one_trip["bags_allowed"] = bag_min
        one_trip["bags_count"] = searched_bags
        one_trip["destination"] = last_ticket["destination"]
        one_trip["origin"] = first_ticket["origin"]
        one_trip["total_price"] = total
        one_trip["travel_time"] = str(travel_time(first_ticket["departure"], last_ticket["arrival"]))

        # -- Adding the trip to the list of the all possible trips --
        json_list.append(one_trip)

    return json_list
