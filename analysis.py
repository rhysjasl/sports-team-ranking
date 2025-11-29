# import libraries
import numpy as np
import pandas as pd
import numpy.linalg as la
from IPython.display import display
from processing import *

# direct method for ranking
def direct_method(A: pd.DataFrame, verbose: bool = False):
    """
    Performs Keener's direct method for calculating rank

    Args:
        A (pd.DataFrame): Preference matrix calculated in processsing steps
        verbose (bool, optional): Turns on verbose mode
                                  If none, defaults to verbose mode off

    Returns:
        r_vec (np.ndarray): Ranking vector based on the largest real, positive eigenvalue and corresponding eigenvector of the A matrix
    """
    # find largest real, positive eigenvalue and corresponding eigenvector
    lam, E = la.eig(A)
    ind = np.argmax(lam.real)
    max_lam = lam[ind].real
    max_E = E[:, ind].real
    if verbose:
        print(f'Largest real, positive eigenvalue: {max_lam}')
        print(f'Corresponding eigenvector: {max_E}')

    # create ranking vector based on max_E
    r_vec = max_E / np.sum(max_E)
    if verbose:
        # verify that ranking vector sums to 1
        print(f'Ranking vector sums to: {np.sum(r_vec)}')

    # return ranking vector
    return r_vec

# define continuous monotone increasing function f(x)
def f_inc(x):
    """
    The continuous monotone increasing function f(x) used in the nonlinear method
    """
    return (0.05*x + x**2) / (2 + 0.05*x + x**2)

# nonlinear method for ranking
def nonlinear_method(teams: pd.Series, S: pd.DataFrame, G: pd.DataFrame, max_iter: int = 100, tol: float = 1e-6, verbose: bool = False):
    """
    Performs Keener's nonlinear method for calculating rank

    Args:
        teams (pd.Series): List of team name abbreviations
        S (pd.DataFrame): Scores matrix with the total number of points scored by team i (rows) against team j (cols) across the entire season
        G (pd.DataFrame): Games matrix with the total number of games played by team i (rows) against team j (cols) across the entire season - will be symmetric!
        max_iter (int, optional): Maximum number of iterations to run through the nonlinear method if convergence is not reached
                                  If none, defaults to 100 iterations
        tol (float, optional): Tolerance threshold for reaching convergence
                               If none, defaults to 1e-6
        verbose (bool, optional): Turns on verbose mode
                                  If none, defaults to verbose mode off

    Returns:
        r (np.ndarray): Ranking vector based on the f matrix composed with f(x) when convergence is reached (or after maximum iterations if convergence not reached)
    """
    # initialize ranking vector
    r = np.ones(len(teams))
    # pre-allocate e matrix
    e = pd.DataFrame(0., index=teams, columns=teams)
    # build f matrix using nonlinear function f(x)
    fmat = pd.DataFrame(0., index=teams, columns=teams)

    for it in range(max_iter):
        # build e matrix from scores
        for i in range(len(teams)):
            for j in range(len(teams)):
                e.iloc[i, j] = (5 + S.iloc[i, j] + (S.iloc[i, j] ** (2/3))) / (5 + S.iloc[j, i] + (S.iloc[j, i] ** (2/3)))
                fmat.iloc[i, j] = f_inc(e.iloc[i, j] * r[j])

        # create ranking vector based on f matrix
        r_new = fmat.sum(axis=1).values / G.sum(axis=1).values

        # check for convergence
        if la.norm(r_new - r, ord=1) < tol:
            print(f'Converged after {it + 1} iterations.')
            return r_new
        
        r = r_new

    # if max_iters reached without convergence
    print('Maximum iterations reached without convergence.')
    return r

def create_ranking(file_path: str, df: pd.DataFrame, max_iter: int = 100, tol: float = 1e-6, verbose: bool = False, save_file: str = None, save_type: str = 'csv'):
    """
    Performs all processing and analysis steps after the season data is loaded to create the final ranking by all methods

    Args:
        file_path (str): The full filepath (direct or relative) to the file containing the teams data
        df (pd.DataFrame): Full season data as a DataFrame with the date, competing teams, final scores, and who won/lost
        max_iter (int, optional): Maximum number of iterations to run through the nonlinear method if convergence is not reached
                                  If none, defaults to 100 iterations
        tol (float, optional): Tolerance threshold for reaching convergence
                               If none, defaults to 1e-6
        verbose (bool, optional): Turns on verbose mode
                                  If none, defaults to verbose mode off
        save_file (str, optional): Location to save the final rankings (without file extension)
                                   If none, defaults to None (will not save ranking)
        save_type (str, optional): File type to save the final rankings as - options: csv, latex
                                   If none, defaults to csv

    Returns:
        final_result (pd.DataFrame): DataFrame containing all teams, total number of wins, and integer rank for number of wins, direct method, and nonlinear method 
                                     DataFrame is sorted first by total number of wins, then by direct rank, then by nonlinear rank
    """
    # import teams data
    teams, teams_list = import_teams_data(file_path=file_path, verbose=verbose)

    # process game data to get preference matrix A
    S, G, W, A = process_game_data(df=df, teams_list=teams_list, method="distribute", verbose=verbose)

    # compute rankings using direct method
    r_direct = direct_method(A=A, verbose=verbose)

    # compute rankings using nonlinear method
    r_nonlinear = nonlinear_method(teams=teams_list, S=S, G=G, max_iter=max_iter, tol=tol, verbose=verbose)

    # add wins column
    wins = W.sum(axis=1).values

    # compile results into a DataFrame
    ranking = pd.DataFrame({'abbr': teams_list, 'Wins': wins, 'Direct Score': r_direct, 'Nonlinear Score': r_nonlinear})
    ranking['Wins Rank'] = ranking['Wins'].rank(method='dense', ascending=False).astype(int)
    ranking['Direct Rank'] = ranking['Direct Score'].rank(method='dense', ascending=False).astype(int)
    ranking['Nonlinear Rank'] = ranking['Nonlinear Score'].rank(method='dense', ascending=False).astype(int)

    # merge with full team names
    result = pd.merge(teams, ranking, on='abbr')
    # select ranks and rename team column
    final_result = result[['team', 'Wins', 'Wins Rank', 'Direct Rank', 'Nonlinear Rank']].sort_values(by='Wins', ascending=False)
    final_result.rename(columns={'team': 'Team'}, inplace=True)

    display(final_result.style.hide(axis='index'))

    # save results if save_file is provided
    if save_file:
        if save_type == 'csv':
            final_result.to_csv(save_file, index=False)
        elif save_type == 'latex':
            final_result.to_latex(save_file, index=False)
        else:
            raise ValueError('Unsupported save type. Please use "csv" or "latex".')

    return final_result