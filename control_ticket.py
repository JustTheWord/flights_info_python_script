from make_json import convert_str_to_date


def bags_check_ok(bags_need, ticket_bags) -> bool:
    return bags_need <= ticket_bags


def layover_time(arrival, departure) -> float:
    return (convert_str_to_date(departure) - convert_str_to_date(arrival))\
               .total_seconds() / 3600 if departure > arrival else 0.0
