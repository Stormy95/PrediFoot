import pandas as pd
import numpy as np
import math
import datetime

df = pd.read_excel('season_1718.xlsx')
# print(df)

class Team:
    # To get HomeMatches do:
    #  HomeMatches = len(self.HomeMarked)
    # the same is valid to AwayMatches

    def __init__(self, Name):
        self.Name = Name
        self.HomeMarked = list()
        self.HomeConceded = list()
        self.HomeMeanMarked = 0
        self.HomeMeanConceded = 0

        self.AwayMarked = list()
        self.AwayConceded = list()
        self.AwayMeanMarked = 0
        self.AwayMeanConceded = 0

    def SetMatches(self,df):
        n = 0
        for y in df['HomeTeam']:
            if(y == self.Name):
                self.HomeMarked.append(float(df['FTHG'][n]))
                self.HomeConceded.append(float(df['FTAG'][n]))
            n += 1
        self.HomeMeanMarked = sum(self.HomeMarked)/max(1,len(self.HomeMarked))
        self.HomeMeanConceded = sum(self.HomeConceded)/max(1,len(self.HomeConceded))

        n = 0
        for y in df['AwayTeam']:
            if(y == self.Name):
                self.AwayMarked.append(float(df['FTAG'][n]))
                self.AwayConceded.append(float(df['FTHG'][n]))
            n += 1
        self.AwayMeanMarked = sum(self.AwayMarked)/max(1,len(self.AwayMarked))
        self.AwayMeanConceded = sum(self.AwayConceded)/max(1,len(self.AwayConceded))

class Season:
    def __init__(self):
        HomeMean = 0
        AwayMean = 0
        Matches = 0

    def SetMeans(self,df):
        n = 0
        mean = 0
        for y in df['FTHG']:
            mean += float(y)
            n += 1

        self.HomeMean = mean/n
        self.Matches = n

        n = 0
        mean = 0
        for y in df['FTAG']:
            mean += float(y)
            n += 1

        self.AwayMean = mean/n

def SetForces(TeamHome,TeamAway,SeasonBPL):
    # The relation between Team/Season is the parameter
    # HomeAtk = HomeMarked/SeasonHomeMarked
    # HomeDef = HomeConceded/SeasonHomeConceded
    # But SeasonHomeConceded = SeasonAwayMarked

    # AwayAtk = AwayMarked/SeasonAwayMarked
    # AwayDef = AwayConceded/SeasonAwayConceded
    # But SeasonAwayConceded = SeasonHomeMarked

    HomeParamAtk = TeamHome.HomeMeanMarked/SeasonBPL.HomeMean
    HomeParamDef = TeamHome.HomeMeanConceded/SeasonBPL.AwayMean

    AwayParamAtk = TeamAway.AwayMeanMarked/SeasonBPL.AwayMean
    AwayParamDef = TeamAway.AwayMeanConceded/SeasonBPL.HomeMean

    LambdaHome = HomeParamAtk*AwayParamDef*SeasonBPL.HomeMean
    LambdaAway = AwayParamAtk*HomeParamDef*SeasonBPL.AwayMean

    return LambdaHome,LambdaAway

def SetLamb(TeamHome,TeamAway,SeasonBPL,df):
    #Calculating Lambda according to the attack and defense pottentials
    Lambda = SetForces(TeamHome,TeamAway,SeasonBPL)

    return Lambda

def SetProb(TeamHome,TeamAway,SeasonBPL,df):
    Lambda = SetLamb(TeamHome,TeamAway,SeasonBPL,df)

    PHome = list() 
    PAway = list()

    #Suposing that the number of goals follow a Poisson's distribution
    for i in range (0,9):
        PHome.append(math.exp(-Lambda[0])*((Lambda[0])**i)/math.factorial(i))
        PAway.append(math.exp(-Lambda[1])*((Lambda[1])**i)/math.factorial(i))

    # Proba is a matrix which it's first entry [i] is P(Home=i)
    # and second entry [j] is P(Away=j)
    Proba = [[0] * 10 for r in range(0,10)]
    for i in range (0,9):
        for j in range (0,9):
            Proba[i][j] = round(100*PHome[i]*PAway[j],2)

    #To calculate probabilities of win/draw/defeat
    ProbHome = 0
    ProbDraw = 0
    ProbAway = 0
    for j in range(0,9):
        for i in range(j+1,9):
            ProbHome += Proba[i][j]

    for i in range(0,9):
        ProbDraw += Proba[i][i]

    for i in range(0,9):
        for j in range(i+1,9):
            ProbAway += Proba[i][j]

    # To discover the winner
    Result = [ProbHome,ProbDraw,ProbAway]
    Result.sort()
    if Result[2] == ProbHome:
        R = 'H'
    elif Result[2] == ProbDraw:
        R = 'D'
    elif Result[2] == ProbAway:
        R = 'A'

    return Proba,ProbHome,ProbDraw,ProbAway,R

def set_prob_bet_odds(n, df):
    betting_name = 'VC'
    
    home_win_prob = df[betting_name + 'H'][n]
    draw_prob = df[betting_name + 'D'][n]
    away_win_prob = df[betting_name + 'A'][n]
    
    if type(home_win_prob) == datetime.datetime:
        home_win_prob = home_win_prob.strftime('%m/%d/%Y')
        home_win_prob_converted = home_win_prob[1] + '.' + home_win_prob[4]
        home_win_prob = float(home_win_prob_converted)
    
    if type(draw_prob) == datetime.datetime:
        draw_prob = draw_prob.strftime('%m/%d/%Y')
        draw_prob_converted = draw_prob[1] + '.' + draw_prob[4]
        draw_prob = float(draw_prob_converted)
    
    if type(away_win_prob) == datetime.datetime:
        away_win_prob = away_win_prob.strftime('%m/%d/%Y')
        away_win_prob_converted = away_win_prob[1] + '.' + away_win_prob[4]
        away_win_prob = float(away_win_prob_converted)
    
    home_win_prob = 1/float(home_win_prob)
    draw_prob = 1/float(draw_prob)
    away_win_prob = 1/float(away_win_prob)
    # To discover the winner
    Result = [home_win_prob,draw_prob,away_win_prob]
    Result.sort()
    if Result[2] == home_win_prob:
        R = 'H'
    elif Result[2] == draw_prob:
        R = 'D'
    else:
        R = 'A'
    
    return None, home_win_prob, draw_prob, away_win_prob, R
    
    

def GetProb(TeamHomeIn,TeamAwayIn,df):
    # Teams from season 17/18
    Teams = df['HomeTeam'].drop_duplicates()

    #Initialize Team's and Season's values
    BPLTeams = []
    for y in Teams:
        InitTeam = Team(y)
        InitTeam.SetMatches(df)
        BPLTeams.append(InitTeam)

    SeasonBPL = Season()
    SeasonBPL.SetMeans(df)

    ######################################

    # To find Home and Away indices in BPLTeams
    for i in range(len(BPLTeams)):
        if BPLTeams[i].Name == TeamHomeIn:
            HoNumber = i

    for i in range(len(BPLTeams)):
        if BPLTeams[i].Name == TeamAwayIn:
            AwNumber = i

    Proba,ProbHome,ProbDraw,ProbAway,_ = SetProb(BPLTeams[HoNumber],BPLTeams[AwNumber],SeasonBPL,df)

    Up = ["H0","H1","H2","H3","H4","H5","H6","H7","H8","H9"]
    Left = ["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9"]

    print('Teams playing:')
    print('Home (H):',BPLTeams[HoNumber].Name)
    print('Away (A):',BPLTeams[AwNumber].Name)
    print('\n')
    print('Probability of scoring (in %):')
    print(pd.DataFrame(Proba, Up, Left))
    print('\n')

    print(f'{BPLTeams[HoNumber].Name} Wins: {ProbHome}')
    print('Draw: %.2f' %ProbDraw)
    print(f'{BPLTeams[AwNumber].Name} Wins: {ProbAway}')


def TestBack(df):
    # Teams from season 17/18
    Teams = df['HomeTeam'].drop_duplicates()

    #Initialize Team's and Season's values
    BPLTeams = []
    for y in Teams:
        InitTeam = Team(y)
        InitTeam.SetMatches(df)
        BPLTeams.append(InitTeam)

    SeasonBPL = Season()
    SeasonBPL.SetMeans(df)
    ######################################

    # For loop to check the result and the prediction
    n = 0
    good = 0
    HoPredict = 0
    DrPredict = 0
    AwPredict = 0

    print(' ','Home   ','Away','Predicted','Real')
    for Home in df['HomeTeam']:
        Away = df['AwayTeam'][n]

        # To find Home and Away indices in BPLTeams
        for i in range(len(BPLTeams)):
            if BPLTeams[i].Name == Home:
                HoNumber = i

        for i in range(len(BPLTeams)):
            if BPLTeams[i].Name == Away:
                AwNumber = i

        # Returns H, D or A
        #Predicted = SetProb(BPLTeams[HoNumber],BPLTeams[AwNumber],SeasonBPL,df)[4]
        Predicted = set_prob_bet_odds(n,df)[4]
        HomeGoals = float(df['FTHG'][n])
        AwayGoals = float(df['FTAG'][n])

        # To see how many times the model predicted H,D,A
        if Predicted == 'H':
            HoPredict += 1
        if Predicted == 'D':
            DrPredict += 1
        if Predicted == 'A':
            AwPredict += 1

        # To compare if the model succeded or not
        if HomeGoals > AwayGoals:
            Real = 'H'
        elif HomeGoals < AwayGoals:
            Real = 'A'
        elif HomeGoals == AwayGoals:
            Real = 'D'

        if Predicted == Real:
            good += 1

        n += 1
        print(n,Home,Away,Predicted,Real)

    good = int(1000*good/n)/10
    HoPredict = int(1000*HoPredict/n)/10
    DrPredict = int(1000*DrPredict/n)/10
    AwPredict = int(1000*AwPredict/n)/10
    print(f'The model achieved {good}% of success')
    print(f'It predicted {HoPredict}% Home wins, {DrPredict}% Draws and {AwPredict}% Away wins')

#-------------------Instructions-----------------------
# To calculate probabilities of Team Home and Team Away
# SetProb('Team Home','Team Away',df)

# To show probabilities of Team Home and Team Away
# GetProb('Team Home','Team Away',df)
# EXEMPLE:
# GetProb('Arsenal','Tottenham',df)
# GetProb('Watford','Chelsea',df)

# To test probabilities of the season, to validate or not the model
# TestBack(df)
#------------------------------------------------------
#-----------------------Main---------------------------

#GetProb('Tottenham','Everton',df)
TestBack(df)