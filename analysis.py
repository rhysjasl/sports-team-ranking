# import libraries
import numpy as np
import pandas as pd
import numpy.linalg as la

# direct method for ranking
def direct_method(A: pd.DataFrame, verbose: bool = False):
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
    return (0.05*x + x**2) / (2 + 0.05*x + x**2)

# nonlinear method for ranking
def nonlinear_method(teams: pd.Series, S: pd.DataFrame, G: pd.DataFrame, max_iter: int = 100, tol: float = 1e-6, verbose: bool = False):
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

