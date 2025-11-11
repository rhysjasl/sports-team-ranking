# 🏆 Sports Team Ranking
Ranking MLB ⚾, NBA 🏀, NFL 🏈 teams using a direct matrix method and a nonlinear method
<br/>

## 🗂️ Repository contains
- MLB, NBA, NFL data sets
    - `xxx_yyyy_season.csv`: Regular season results for specified league, including date game was played, scores for away and home teams, and winner/loser
    - `xxx_conferences.csv`: List of teams in the league with their associated conference and region
    - `xxx_stats.csv`: List of teams with their cumulative scores as home vs. away team, and total score of the entire regular season with the number of wins and losses
    - `xxx_teams.csv`: List of teams in the league with both full name and abbreviation
    - <strong>Note:</strong> scores were copied by hand, then `xxx_stats.csv` was used to verify against the official websites of each respective league

- Processing notebook: Exploration of an individual data set through the necessary processing steps
- `processing.py`: same processing steps as the notebook, structured as functions to be used in the analysis steps
- Analysis notebook: Exploration of an individual data set through both analysis methods
- `analysis.py`: same analyses as the notebook, structured as function to be reused

## 💻 How To Use
