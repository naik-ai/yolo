from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    User Telgram users who join the group in which bot is added.

    Args:
        SQLModel (_type_):
        table (bool, optional): Defaults to True
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    telegram_id: int
    telegram_username: str
    join_date: str = datetime.now()


class IPLSchedule(SQLModel, table=True):
    """
    Command: `/show_ipl_schedule`
    Description: show the ipl schedule with date, time, and venue and names of teams
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    venue: str
    team1: str
    team2: str


class PlayerStats(SQLModel, table=True):
    """
    Command: `/show_leatherboard`
    Description: show the leatherboard with players and their stats
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    player_name: str
    matches_played: int
    runs: int
    wickets: int
    highest_score: int
    best_bowling: str  # Assuming format like "5/24"


class MatchStats(SQLModel, table=True):
    """
    Command: `/show_current_match_stats`
    Description: show the current match stats
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int  # Assuming this links to an IPLSchedule or similar
    team1_score: str  # Assuming format like "164/8"
    team2_score: str
    match_winner: str
    player_of_the_match: str


class MatchPoll(SQLModel, table=True):
    """
    Command: `/create_next_match_poll`
    Description: create a poll for the next match
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int  # Assuming this links to an IPLSchedule or similar
    poll_question: str
    poll_options: str  # This could be a JSON string of options


class PollResults(SQLModel, table=True):
    """
    Command: `/poll_results`
    Description: show the poll results
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: int  # Assuming this links to a MatchPoll
    option: str
    votes: int


class GamePitchAnalysis(SQLModel, table=True):
    """
    Command: `/game_pitch_analysis`
    Description: show the game pitch analysis
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int  # Assuming this links to an IPLSchedule or similar
    pitch_condition: str
    expected_outcome: str
