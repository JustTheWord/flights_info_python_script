from datetime import datetime


def bags_check_ok(bags_need, ticket_bags) -> bool:
    return bags_need <= ticket_bags


def layover_time(arrival, departure) -> float:
    # the arrival date partitioned to the date and the precise time
    date, _, time = arrival.rpartition('T')
    year, month, day = map(lambda s: int(s), date.split('-'))
    hours, minutes, seconds = map(lambda s: int(s), time.split(':'))
    arrival = datetime(year, month, day, hours, minutes, seconds)
    # the departure date partitioned to the date and the precise time
    date, _, time = departure.rpartition('T')
    year, month, day = map(lambda s: int(s), date.split('-'))
    hours, minutes, seconds = map(lambda s: int(s), time.split(':'))
    departure = datetime(year, month, day, hours, minutes, seconds)
    # finding the total time of the layover in hours
    return (departure - arrival).total_seconds() / 3600 if departure > arrival else 0.0
