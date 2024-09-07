#!/usr/bin/env python3
from requests import post
import logging
from tornado.options import options

tables = [
    "The Oyster Club",
    "Bonjour le monde",
    "Default",
    "méchante pomme 2",
    "CollineduCr'Hack",
    "Hackcess",
    "PastisPétanque",
    "DEHACK ESPORT",
    "Pand'Hack",
    "VHackances",
    "N2A",
    "K'Hack App Root",
    "la roche sur hack",
    "Redmine3",
    "Les 4 Fantastiques",
    "Tarm'hacj",
    "csiml",
    "Noobworld"
]

API_BASE=options.led_base_api
ROUND_DURATION=30

def get_table_id_by_team_name(team_name):
    return tables.index(team_name)+1

def led_flag(team_name):
    rq = post(API_BASE+"flag", json={"table": get_table_id_by_team_name(team_name)})
    if rq.status_code != 200:
        logging.error(f"{API_BASE}flag not reachable !!! Team_name: {team_name} | status_code: {rq.status_code}")


def led_own(team_name):
    rq = post(API_BASE+"box", json={"table": get_table_id_by_team_name(team_name)})
    if rq.status_code != 200:
        logging.error(f"{API_BASE}box not reachable !!! Team_name: {team_name} | status_code: {rq.status_code}")

ROUND = 1
def led_round_start():
    global ROUND
    if ROUND == 4:
        rq = post(API_BASE+"round", json={"duration": ROUND_DURATION, "round": "finale"})
    else:
        rq = post(API_BASE+"round", json={"duration": ROUND_DURATION, "round": ROUND})

    if rq.status_code != 200:
        logging.error(f"{API_BASE}round not reachable !!! Can't start box. | | status_code: {rq.status_code}")
    ROUND+=1

def led_stop():
    rq = post(API_BASE+"forceColor", json={"duration": 10, "color": "#1fe4f7"})
    if rq.status_code != 200:
        logging.error(f"{API_BASE}round not reachable !!! Can't start box. | | status_code: {rq.status_code}")

if __name__ == '__main__':
    led_flag("Bonjour le monde")  # Should not log errors

    # Test own function
    led_own("Bonjour le monde")  # Should not log errors

    # Test round_start function
    led_round_start()  # Should not log errors
