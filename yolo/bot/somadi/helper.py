from enum import Enum, auto
from typing import List

team_names_to_short = {
    "Mumbai Indians": "MI",
    "Delhi Capitals": "DC",
    "Kolkata Knight Riders": "KKR",
    "Chennai Super Kings": "CSK",
    "Royal Challengers Bengaluru": "RCB",
    "Punjab Kings": "PBKS",
    "Sunrisers Hyderabad": "SRH",
    "Rajasthan Royals": "RR",
    "Lucknow Super Giants": "LSG",
    "Gujarat Titans": "GT",
}


class Team(Enum):
    CSK = auto()
    KKR = auto()
    RCB = auto()
    SRH = auto()
    PBKS = auto()
    RR = auto()
    DC = auto()
    LSG = auto()
    MI = auto()


def list_teams(selected_teams: List[Team]) -> None:
    for team in selected_teams:
        print(team.name)


def get_team_from_string(team_str: str) -> Team:
    try:
        return Team[team_str.upper()]
    except KeyError:
        raise ValueError(f"Unknown team: {team_str}")
