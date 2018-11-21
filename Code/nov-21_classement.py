import matplotlib.pyplot as plt
import numpy as np
import json
import csv
from slugify import slugify
from matplotlib.font_manager import FontProperties

def csv_to_list(odds_file,season):
    # Checks if file odds exists
    try:
        with open(odds_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except:
        print('Error! File odds matches for season %i not found!' %season)
        print('PROGRAM STOPPED')
        quit()

    odds_full = rows

    odds_new = []
    for match in odds_full:
        date = match["Date"]

        hometeam = match["HomeTeam"]
        awayteam = match["AwayTeam"]

        homegoals = int(match["FTHG"])
        awaygoals = int(match["FTAG"])

        home_odds = float(match["PSH"])
        draw_odds = float(match["PSD"])
        away_odds = float(match["PSA"])

        odds = [home_odds,draw_odds,away_odds]

        # Creates a new dictionary
        match_dict = {"date" : date, "home team": hometeam, "away team": awayteam, "home goals": homegoals,
        "away goals": awaygoals, "odds hda": odds}
        odds_new.append(match_dict)

    return odds_new

def sim_match(home_team,away_team):
    rand = np.random.rand()
    if rand >= 0 and rand < 1/3:
        R = 'H'
    elif rand >= 1/3 and rand < 2/3:
        R = 'H'
    elif rand >= 2/3 and rand <= 1:
        R = 'A'

    # Return R = 'H','D' or 'A'
    # 'H' : Home wins
    # 'D' : Draw
    # 'A' : Away wins
    return R

def get_points(n_round,teams,matches):
    # Points for each team / round
    points = {key: [0]*(n_round+1) for key in teams}

    for team in teams:
        n = 0
        for match in matches:
            home_team = match["home team"]
            away_team = match["away team"]

            if home_team == team:
                match_result = sim_match(home_team,away_team)

                n += 1
                if match_result == 'H': # Home wins : +3
                    points[home_team][n] = points[home_team][n-1] + 3
                elif match_result == 'D': # Draw : +1
                    points[home_team][n] = points[home_team][n-1] + 1
                elif match_result == 'A' : # Away wins: +0
                    points[home_team][n] = points[home_team][n-1]

            elif away_team == team:
                match_result = sim_match(home_team,away_team)

                n += 1
                if match_result == 'A': # Away wins : +3
                    points[away_team][n] = points[away_team][n-1] + 3
                elif match_result == 'D': # Draw : +1
                    points[away_team][n] = points[away_team][n-1] + 1
                elif match_result == 'H' : # Home wins: +0
                    points[away_team][n] = points[away_team][n-1]

            #if team == "Chelsea":
            #    print(match["date"],n,points["Chelsea"][n])

        try:
            assert n == n_round,"Error! Check matches file"
        except AssertionError as e:
            message = e.args[0]
            message += "\nTeam "+ team + " has played ",n," rounds"
            message += '\n but there are ',n_round,' rounds'
            message += '\n PROGRAM STOPPED'

            e.args = (message,)
            raise

    return points

def plot_graph(n_round,teams,points):
    plot_teams = {key: [] for key in teams}

    xplot = [i for i in range(n_round+1)]
    for team in teams:
        yplot = [0]*(n_round+1)
        for n in range(n_round+1):
            yplot[n] = points[team][n]

        plot_teams[team].append(yplot)

    ymax = 0
    for point in plot_teams:
        p_last_round = plot_teams[point][0][n_round]
        ymax = max(ymax,p_last_round)

    ymax = ymax + 5

    plot_list = []
    for team in teams:
        x = xplot
        y = plot_teams[team][0]
        pos_x = 1.0
        pos_y = y[n_round]/ymax

        dict = {
                'x': x,
                'y': y,
                'pos_x': pos_x,
                'pos_y': pos_y,
                'label': team,
                }

        plot_list.append(dict)
    # Change x for same x_plot
    for dict in plot_list:
        x1 = dict["x"]
    for i in range(len(plot_list)):
        x1 = plot_list[i]["pos_x"]
        for j in range(i+1,len(plot_list)-1):
            x2 = plot_list[j]["pos_x"]
    ###### Not finished
    # Plot
    for dict in plot_list:
        x = dict["x"]
        y = dict["y"]
        pos_x = dict["pos_x"]
        pos_y = dict["pos_y"]
        label = dict["label"]

        line, = plt.plot(x,y,label = label)
        legend = plt.legend(handles=[line],loc='center left',frameon=False,bbox_to_anchor=(pos_x, pos_y))
        ax = plt.gca().add_artist(legend)

    # Configurations
    #plt.xticks(np.arange(0, n_round+1, step=1))
    plt.xlim(0,n_round)
    plt.ylim(0,ymax)
    plt.grid(axis='both')

    #plt.legend(frameon=False)
    plt.show()

def graph_table(file,season):
    # Transforms the .csv into a dictionary
    matches = csv_to_list(file,season)

    #
    n_matches = len(matches)
    n_round = int(n_matches/10)
    if int(n_round)-(n_matches/10) != 0:
        print("\n")
        print("Error! Number of matches not a multiple of 10, round is not finished")
        print('PROGRAM STOPPED')
        quit()

    # Get teams' names
    teams = []
    for match in matches:
        name = match["home team"]
        if len(teams) == 0:
            teams.append(name)
        else:
            if name not in teams:
                teams.append(name)

    # Check if there are 20 teams in the file
    assert len(teams) == 20, print('There are not 20 teams in this file, PROGRAM STOPPED')
    points = get_points(n_round,teams,matches)
    plot_graph(n_round,teams,points)

#########################################################################
# Season
season = 16

# Path of odds (matches) file
path_odds = 'C:\\Users\\Samsung\\Desktop\\PE\\log\\seances\\nov_21\\'

# File name should be:
# EX: season_16.csv
odds_file = path_odds + 'season_' + str(season) + '.csv'
#########################################################################

graph_table(odds_file,season)
