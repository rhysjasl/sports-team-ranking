# 🏆 Sports Team Ranking
✨ Ranking MLB ⚾, NBA 🏀, NFL 🏈 teams using a direct matrix method and a nonlinear method ✨ <br/>
This analysis uses the methods outlined by James Keener in his 1993 paper, "The Perron-Frobenius theorem and the ranking of football teams". The direct method creates a ranking vector from the eigenvector that corresponds to the largest real, positive eigenvalue of the preference matrix A, which is determined by the outcome of all games. The nonlinear method creates a matrix from the scores of each game and passes that through a continuous monotone increasing function to recursively produce a ranking vector until convergence is reached.
<br/>

## 🗂️ Repository contains
- MLB, NBA, NFL data sets
    - `xxx_yyyy_season.csv`: Regular season results for specified league, including date game was played, scores for away and home teams, and winner/loser
    - `xxx_conferences.csv`: List of teams in the league with their associated conference and region
    - `xxx_stats.csv`: List of teams with their cumulative scores as home vs. away team, and total score of the entire regular season with the number of wins and losses
    - `xxx_teams.csv`: List of teams in the league with both full name and abbreviation
    - <strong>Note:</strong> Scores were copied by hand, then `xxx_stats.csv` was used to verify against the official websites of each respective league

- `processing.ipynb`: Exploration of an individual data set through the necessary processing steps in notebook form
- `processing.py`: Same processing steps as the notebook, structured as functions to be used in the analysis steps
- `analysis.ipynb`: Exploration of an individual data set through both analysis methods in notebook form
- `analysis.py`: Same analyses as the notebook, structured as function to be reused
- `results.ipynb`: Notebook that calls processing and analysis functions for multiple data files

## 💻 How To Use
- To run multiple files through these methods, please consult the Results Notebook.
- If you would like to more thoroughly explore each step of the methods, please consult the Processing and Analysis Notebooks.
- If you would like to use these methods in your own code to analyze your own data, feel free to import the functions defined in the `processing.py` and `analysis.py` files. 
>[!CAUTION]
>Pay attention to how the example data sets have been structured if you would like to use these functions with your own data, as the functions call certain named columns from the example data sets

## 📖 Reference
Keener, J. P. (1993). The Perron-Frobenius theorem and the ranking of football teams. SIAM review, 35(1), 80-93.
