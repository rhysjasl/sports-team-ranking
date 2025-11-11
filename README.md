# sports-team-ranking
Ranking MLB, NBA, NFL teams using a direct matrix method and a nonlinear method
<br/>

## Repository contains
<ul>
    <li>MLB, NBA, NFL data sets</li>
    <ul>
        <li>`xxx_yyyy_season.csv`: Regular season results for specified league, including date game was played, scores for away and home teams, and winner/loser</li>
        <li>`xxx_conferences.csv`: List of teams in the league with their associated conference and region</li>
        <li>`xxx_stats.csv`: List of teams with their cumulative scores as home vs. away team, and total score of the entire regular season with the number of wins and losses</li>
        <li>`xxx_teams.csv`: List of teams in the league with both full name and abbreviation</li>
        <li><strong>Note:</strong> scores were copied by hand, then `xxx_stats.csv` was used to verify against the official websites of each respective league</li>
    </ul>
    <li>Processing notebook: Exploration of an individual data set through the necessary processing steps</li>
    <li>`processing.py`: same processing steps as the notebook, structured as functions to be used in the analysis steps</li>
    <li>Analysis notebook: Exploration of an individual data set through both analysis methods</li>
    <li>`analysis.py`: same analyses as the notebook, structured as function to be reused</li>
</ul>

## How To Use
