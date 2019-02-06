import T00_cons

import numpy as np
import json
import csv

##################################################################
#                          01_TREATMENT
def check_files(league,seasonI,seasonO):
    for season in range(seasonI,seasonO+1):
        path_teams = './data/'+ league +'/FIFA/'
        teams_file = path_teams + 'team_stats_fifa_' + str(season+1) + '.json'

        path_odds = './data/'+ league +'/odds/'
        odds_file = path_odds + 'season_' + str(season) + '.csv'

        # Checks if there is a teams file
        try:
            with open(teams_file) as json_file:
                teams = json.load(json_file)
        except:
            print('Error! File team stats for league ',league,' and fifa %i not found!' %(season+1))
            quit()

        # Checks if file odds exists
        try:
            with open(odds_file) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except:
            print('Error! File odds matches for league ',league,' and season %i not found!' %season)
            quit()

def csv_to_list(league,season):
    path_odds = './data/'+ league + '/odds/'
    odds_file = path_odds + 'season_' + str(season) + '.csv'

    with open(odds_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    odds_full = rows

    odds_new = []
    for match in odds_full:
        date = match["Date"]

        hometeam = match["HomeTeam"]
        awayteam = match["AwayTeam"]

        homegoals = int(match["FTHG"])
        awaygoals = int(match["FTAG"])

        try:
            home_odds = float(match["PSH"])
            draw_odds = float(match["PSD"])
            away_odds = float(match["PSA"])
        except:
            home_odds = float(match["B365H"])
            draw_odds = float(match["B365D"])
            away_odds = float(match["B365A"])

        odds = [home_odds,draw_odds,away_odds]

        if homegoals > awaygoals:
            result = [1,0,0]
        elif homegoals == awaygoals:
            result = [0,1,0]
        elif homegoals < awaygoals:
            result = [0,0,1]

        # Find min odds -> max prob
        min_odd_index = odds.index(min(odds))
        # Find max prob -> the outcome
        max_result_index = result.index(max(result))

        # If ==, then match was predicted by odds
        if min_odd_index == max_result_index:
            predict = 'y'
        else:
            predict = 'n'

        match_dict = {
        "date" : date,
        "home team": hometeam,
        "away team": awayteam,
        "home goals": homegoals,
        "away goals": awaygoals,
        "odds hda": odds,
        "result hda": result,
        "predict": predict
        }

        odds_new.append(match_dict)

    # Change team's names
    try:
        list_cons = T00_cons.ALL_TEAMS[league]
    except:
        print('Error! File cons does not have dict ',league)
        quit()

    for match in odds_new:
        hometeam = match["home team"]
        awayteam = match["away team"]

        odds_new[odds_new.index(match)]["home team"] = list_cons[1][hometeam]
        odds_new[odds_new.index(match)]["away team"] = list_cons[1][awayteam]

    return odds_new

def add_fifa(matches,league,season):
    path_teams = './data/'+ league + '/FIFA/'
    teams_file = path_teams + 'team_stats_fifa_' + str(season+1) + '.json'

    with open(teams_file) as json_file:
        teams = json.load(json_file)

    for match in matches:
        hometeam = match["home team"]
        awayteam = match["away team"]

        for team in teams:
            if team["name"] == hometeam:
                home_fifa = [team["att"],team["mid"],team["def"]]

            if team["name"] == awayteam:
                away_fifa = [team["att"],team["mid"],team["def"]]

        try:
            index = matches.index(match)
            matches[index]["home fifa"] = home_fifa
            matches[index]["away fifa"] = away_fifa
        except:
            print(match)
            print('Error! One of these 2 teams was not found')
            print('Season: ',season)
            print(hometeam,awayteam)
            quit()

    return matches

def add_lambda(matches):
    teams = []
    for match in matches:
        team = match["home team"]
        if team not in teams:
            teams.append(team)

    assert len(teams) == 20, "Error! Season does not have 20 teams"

    # How many matches matter
    streak = 3

    for team in teams:
        goals_marked = [0] * streak
        goals_received = [0] * streak
        count = 0

        for n in range(len(matches)):
            count_streak = count % streak
            home_team = matches[n]["home team"]
            away_team = matches[n]["away team"]

            home_goals = matches[n]["home goals"]
            away_goals = matches[n]["away goals"]

            if team == home_team:
                count += 1

                lambda_atk = 0
                for i in goals_marked:
                    lambda_atk += i
                matches[n]["lambda atk"] = lambda_atk
                goals_marked[count_streak] = home_goals


                lambda_def = 0
                for i in goals_received:
                    lambda_def += i
                matches[n]["lambda def"] = lambda_def
                goals_received[count_streak] = away_goals
                #print('HOME',result,count,count_streak,points_streak,matches[n]["home streak"])
            elif team == away_team:
                
                a = 1

    return matches

def save_matches_json(league,season,matches):
    path = './data/'+ league + '/odds/'
    file = path + 'matches_season_' + str(season) + '.json'

    # Save a json with a new list
    with open(file, 'w') as json_file:
        json.dump(matches, json_file)

##################################################################
#                        02_GET IN OUT
def get_in_from_match(match):
    input_home = match["home fifa"]
    input_away = match["away fifa"]

    input = input_home + input_away
    return input

def get_out_from_match(match,choose):
    if choose == 1: # Output = Odds
        output = match["odds hda"]
    elif choose == 2: # Output = Result(3)
        output = match["result hda"]
    elif choose == 3: # Output = Result(5), Big wins/losses
        h_g = match["home goals"]
        a_g = match["away goals"]

        dif_g = h_g - a_g

        if dif_g >= 3:
            output = [1,0,0,0,0]
        elif dif_g == 2:
            output = [0.5,0.5,0,0,0]
        elif dif_g == 1:
            output = [0,1,0,0,0]
        elif dif_g == 0:
            output = [0,0,1,0,0]
        elif dif_g == -1:
            output = [0,0,0,1,0]
        elif dif_g == -2:
            output = [0,0,0,0.5,0.5]
        elif dif_g <= -3:
            output = [0,0,0,0,1]
    else:
        print('Error! Choose a model for the output!')
        print('Program T00_funcs -> func -> get_out_from_match')
        quit()

    return output

def generate_inout(league,season):
    path = './data/'+ league + '/odds/'
    matches_file = path + 'matches_season_' + str(season) + '.json'

    with open(matches_file) as json_file:
        matches = json.load(json_file)

    # Loop matches
    list_in = []
    list_out_odds = []
    list_out_result3 = []
    list_out_result = []

    for match in matches:
        input = get_in_from_match(match)
        output_odds = get_out_from_match(match,1)
        output_result3 = get_out_from_match(match,2)
        output_result = get_out_from_match(match,3)

        list_in.append(input)
        list_out_odds.append(output_odds)
        list_out_result3.append(output_result3)
        list_out_result.append(output_result)

    return list_in,list_out_odds,list_out_result3,list_out_result

def save_inout_txt(league,season,list_in,list_out_odds,list_out_result3,list_out_result):
    # Create output files
    path_inout = './data/'+ league + '/vectors/'

    input_file = path_inout + 'in_season_' + str(season) + '.txt'
    out_odds_file = path_inout + 'out_odds_season_' + str(season) + '.txt'
    out_result3_file = path_inout + 'out_result3_season_' + str(season) + '.txt'
    out_result_file = path_inout + 'out_result_season_' + str(season) + '.txt'

    with open(input_file,"w+") as f:
        for item in list_in:
            for i in range(len(item)):
                f.write("%s " % item[i])
            f.write("\n")

    with open(out_odds_file,"w+") as f:
        for item in list_out_odds:
            for i in range(len(item)):
                f.write("%s " % item[i])
            f.write("\n")

    with open(out_result3_file,"w+") as f:
        for item in list_out_result3:
            for i in range(len(item)):
                f.write("%s " % item[i])
            f.write("\n")

    with open(out_result_file,"w+") as f:
        for item in list_out_result:
            for i in range(len(item)):
                f.write("%s " % item[i])
            f.write("\n")

##################################################################
#                        03_TF CHRIS

##################################################################
#                        04_TF TEST
