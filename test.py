import pandas as pd

df = pd.read_excel('E0.xlsx')


home_goals = df.loc[df['HomeTeam']=="Arsenal"]['FTHG'].sum()
away_goals = df.loc[df['AwayTeam']=="Arsenal"]['FTAG'].sum()
match_count = df.loc[df['HomeTeam']=="Arsenal"].shape[0]
match_count2 = df.loc[df['AwayTeam']=="Arsenal"].shape[0]

match_count_total = match_count + match_count2

goal_average = (home_goals + away_goals)/match_count_total

print(goal_average)

