import argparse
import csv

from collections import defaultdict

DEFAULT_ROUTE_TYPE = "sport"
GRADES_ORDER = [
    "3rd", "4th", "5.0", "5.1", "5.2", "5.3",
    "5.4", "5.5", "5.6", "5.7", "5.8", "5.9",
    "5.10-", "5.10a", "5.10b", "5.10", "5.10+", "5.10c", "5.10d",
    "5.11-", "5.11a", "5.11b", "5.11", "5.11+", "5.11c", "5.11d",
    "5.12-", "5.12a", "5.12b", "5.12", "5.12+", "5.12c", "5.12d",
    "5.13-", "5.13a", "5.13b", "5.13", "5.13+", "5.13c", "5.13d",
    "5.14-", "5.14a", "5.14b", "5.14", "5.14+", "5.14c", "5.14d",
    "5.15-", "5.15a", "5.15b", "5.15", "5.15+", "5.15c", "5.15d",
]
LEAD_SENDS = ["Redpoint", "Onsight", "Flash", "Pinkpoint"]
PROTECTION_RATINGS = ["PG13", "R", "X"]
TICKS_FILE = "ticks.csv"


def get_grade(grade: str) -> str:
    """
    Climbing grades sometimes have protection ratings on them, ex: '5.9 R'
    For pyramid purposes, we don't really care about this.

    This method removes the protection rating from the grade if it's present, 
    and returns the cleaned grade.
    """

    grade_split = grade.split()
    if len(grade_split) > 1 and grade_split[1] in PROTECTION_RATINGS:
        return grade_split[0]

    return grade


def is_requested_route_type(requested_route_type: str, current_route_type: str) -> bool:
    """
    Routes in Mountain Project can be classified as Sport, Trad, Boulder, TR, Alpine,
    Aid, Solo, or any combination of these (represented as a comma-separated list).

    This method returns whether the current route type could be classified as the
    route type requested by the user.

    So for example, a route that's marked as 'Sport, TR' would be classified as a
    sport climb but not a trad climb; whereas a route that's 'Sport, Trad' (looking at
    you, Zee Tree) is both a sport and a trad climb.
    """

    return requested_route_type.lower() in map(lambda x: x.lower(), current_route_type.split(", "))


def print_climbing_pyramid(climbing_pyramid: dict):
    import pprint

    pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
    pp.pprint(climbing_pyramid)


def sort_by_grade(climbing_pyramid: dict) -> dict:
    climbing_pyramid_sorted = {
        key: climbing_pyramid[key] for key in GRADES_ORDER if key in climbing_pyramid}

    return climbing_pyramid_sorted


if __name__ == "__main__":
    climbing_pyramid = defaultdict(set)
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--type", type=str, required=False, help="Either 'sport' or 'trad'")

    args = parser.parse_args()
    route_type = args.type if args.type else DEFAULT_ROUTE_TYPE

    with open(TICKS_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if is_requested_route_type(route_type, row["Route Type"]) and row["Lead Style"] in LEAD_SENDS:
                climbing_pyramid[get_grade(row["Rating"])].add(row["Route"])

    climbing_pyramid_sorted = sort_by_grade(climbing_pyramid)

    print_climbing_pyramid(climbing_pyramid_sorted)
