# import libraries
import numpy as np
import pandas as pd
from IPython.display import display

def import_league_data(file_path: str, verbose: bool = False):
    # import league data
    df = pd.read_csv(file_path)
    # turn date column into datetime object
    df['date'] = pd.to_datetime(df['date'])
    nrows, ncols = df.shape

    if verbose:
        display(df.head())
        print(f'The dataset has {nrows} rows and {ncols} columns.')

    return df, nrows, ncols

def import_teams_data(file_path: str, verbose: bool = False):
    # import list of teams
    teams = pd.read_csv(file_path)
    teams_list = teams['abbr']
    if verbose: 
        display(teams.head())

    return teams, teams_list

def process_game_data(df: pd.DataFrame, teams_list: pd.Series, method: str = "distribute", verbose: bool = False):
    nrows, ncols = df.shape

    # pre-allocate scores S, games G, wins W matrices
    scores_matrix = pd.DataFrame(0, index=teams_list, columns=teams_list)
    games_matrix = pd.DataFrame(0, index=teams_list, columns=teams_list)
    wins_matrix = pd.DataFrame(0, index=teams_list, columns=teams_list)

    # fill matrices with head-to-head results
    # go down teams list
    for team in teams_list:
        # go through each row in dataset
        for row in range(nrows):
            # if team is away team, update games and wins
            if df.loc[row, 'away'] == team:
                scores_matrix.loc[team, df.loc[row, 'home']] += df.loc[row, 'away-score']
                scores_matrix.loc[df.loc[row, 'home'], team] += df.loc[row, 'home-score']
                games_matrix.loc[team, df.loc[row, 'home']] += 1
                if df.loc[row, 'win'] == team:
                    wins_matrix.loc[team, df.loc[row, 'home']] += 1
            # if team is home team, update games and wins
            elif df.loc[row, 'home'] == team:
                scores_matrix.loc[team, df.loc[row, 'away']] += df.loc[row, 'home-score']
                scores_matrix.loc[df.loc[row, 'away'], team] += df.loc[row, 'away-score']
                games_matrix.loc[team, df.loc[row, 'away']] += 1
                if df.loc[row, 'win'] == team:
                    wins_matrix.loc[team, df.loc[row, 'away']] += 1

    if verbose:
        print("Scores Matrix:")
        display(scores_matrix)
        print("Games Matrix:")
        display(games_matrix)
        print("Wins Matrix:")
        display(wins_matrix)

    # construct preference matrix A
    if method == "all":
        n = games_matrix.sum(axis=1)
        A_matrix = wins_matrix.divide(n).fillna(0)
    if method == "distribute":
        A_matrix = pd.DataFrame(0., index=teams_list, columns=teams_list)
        for team in teams_list:
            for row in range(nrows):
                # if team is away team, add outcome to ij
                if df.loc[row, 'away'] == team:
                    A_matrix.loc[team, df.loc[row, 'home']] += ((scores_matrix.loc[team, df.loc[row, 'home']] + 1) / (scores_matrix.loc[team, df.loc[row, 'home']] + scores_matrix.loc[df.loc[row, 'home'], team] + 2))
                # if team is home team, add outcome to ij
                elif df.loc[row, 'home'] == team:
                    A_matrix.loc[team, df.loc[row, 'away']] += ((scores_matrix.loc[team, df.loc[row, 'away']] + 1) / (scores_matrix.loc[team, df.loc[row, 'away']] + scores_matrix.loc[df.loc[row, 'away'], team] + 2))

    if verbose:
        print("Preference Matrix A:")
        display(A_matrix)
    
    return scores_matrix, games_matrix, wins_matrix, A_matrix