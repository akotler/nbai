import datetime
import logging

from util import database_util
from util.basic import log_call_stack

from web_api.game_logs import get_player_game_logs, get_team_game_logs

now = datetime.datetime.utcnow()
CURRENT_SEASON_YEAR = now.year if now.month > 8 else now.year - 1


"""
Populates the database with player info and game info.
Given a range of [start_season, end_season), this populates
the Schedules, Players, Teams, PlayerGameLog, and TeamGameLog
collections with the appropriate data.

Does not add duplicates, so if this is run multiple times in succession
no data duplication errors will arise.
"""
@log_call_stack
def backfill_server(start_year=2007, end_year=CURRENT_SEASON_YEAR, update_bios=True):

    ## Create all the teams (without active rosters)
    database_util.create_and_save_all_team_records()

    ## Create a dict to store PlayerRecords (for database efficiency)
    player_dict = {}

    ## For each year in the date range we want to fill:
    for year in range(start_year, end_year):

        ## Get all the PlayerGameLogs and TeamGameLogs
        player_game_logs = get_player_game_logs(year)
        team_game_logs = get_team_game_logs(year)

        ## Add all the Players from this season to the database
        database_util.create_and_save_all_player_records(player_game_logs, year, player_dict)

        ## Add all the PlayerGameLogs from this season to the database
        database_util.create_and_save_all_player_game_log_records(player_game_logs)

        ## Add all the TeamGameLogs from this season to the database
        team_game_rosters = database_util.get_team_game_rosters(player_game_logs)
        database_util.create_and_save_all_team_game_log_records(team_game_logs, team_game_rosters)

    ## Now, update current rosters and player biographical data
    database_util.update_rosters()
    database_util.update_player_bios(full_bio=update_bios)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    backfill_server()
