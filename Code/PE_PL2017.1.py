#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 17:51:33 2018

@author: louisladuve
"""

import pandas as pd
from math import *
import numpy as np
import random
from datetime import *
from datetime import datetime

tab = pd.read_excel('SaisonPL2017.xlsx')
tab2018 = pd.read_excel('SaisonPL2018_2019_encours.xlsx')
tab2017and2018 = pd.read_excel('SaisonsPL2017and2018.xlsx')
calendrier_PL2018 = pd.read_excel('Classeur3.xlsx')



changement_nom_equipes(tab,equipescal,equipesres)

# Calcul nombre de but total de l'equipe home marqués à domicile durant la saison 
def calcul_nb_but_dom(tab , equipe):
    home_goals = tab.loc[tab['HomeTeam']== equipe]['FTHG'].sum()
    return home_goals

# Calcul nombre de but total de l'equipe away marqués à l'extérieur durant la saison 
def calcul_nb_but_ext(tab,equipe):
    away_goals = tab.loc[tab['AwayTeam']==equipe]['FTAG'].sum()
    return away_goals

def potentiel_attaque_dom(tab,equipe):
    home_match_count = tab.loc[tab['HomeTeam']==equipe].shape[0]
    return calcul_nb_but_dom(tab,equipe)/home_match_count

def potentiel_attaque_ext(tab,equipe):
    away_match_count = tab.loc[tab['AwayTeam']==equipe].shape[0]
    return calcul_nb_but_ext(tab,equipe)/away_match_count

def calcul_nb_but_pris_dom(tab,equipe):
    home_goals_taken = tab.loc[tab['HomeTeam']== equipe]['FTAG'].sum()
    return home_goals_taken

def calcul_nb_but_pris_ext(tab,equipe):
    away_goals_taken = tab.loc[tab['AwayTeam']== equipe]['FTHG'].sum()
    return away_goals_taken
    
def potentiel_defense_dom(tab,equipe):
    home_match_count = tab.loc[tab['HomeTeam']==equipe].shape[0]
    return calcul_nb_but_pris_dom(tab,equipe)/home_match_count

def potentiel_defense_ext(tab,equipe):
    away_match_count = tab.loc[tab['AwayTeam']==equipe].shape[0]
    return calcul_nb_but_pris_ext(tab,equipe)/away_match_count

def get_teams_list(tab):
    return tab['HomeTeam'].drop_duplicates()

def write_data_excel(tab):
    writer = pd.ExcelWriter('output.xlsx')
    new_tab = get_teams_list(tab)
    new_tab.to_excel(writer, index=False)

#write_data_excel(tab)

# Calcul nombre de but total marqués à domicile durant la saison 
def nombre_moyen_but_ligue_dom(tab):
    total_home_goals = tab['FTHG'].sum() 
    total_match_count = tab['FTHG'].shape[0]
    
    return total_home_goals / total_match_count

# Calcul nombre de but total marqués à l'extérieur durant la saison
def nombre_moyen_but_ligue_ext(tab):
    total_away_goals = tab['FTAG'].sum() 
    total_match_count = tab['FTAG'].shape[0]
    
    return total_away_goals / total_match_count



def force_attaque_dom(tab,equipe):
    return  potentiel_attaque_dom(tab,equipe) / nombre_moyen_but_ligue_dom(tab)
    
def force_attaque_ext(tab,equipe):
    return  potentiel_attaque_ext(tab,equipe) / nombre_moyen_but_ligue_ext(tab)

def force_defense_dom(tab,equipe):
    return  potentiel_defense_dom(tab,equipe) / nombre_moyen_but_ligue_ext(tab) 

def force_defense_ext(tab,equipe):
    return  potentiel_defense_ext(tab,equipe) / nombre_moyen_but_ligue_dom(tab)




#  --------- Parametre lambda de la loi de poisson ----------

def lambda_dom(tab,equipe_dom,equipe_ext):
    return force_attaque_dom(tab,equipe_dom) * force_defense_ext(tab,equipe_ext) * nombre_moyen_but_ligue_dom(tab)

def lambda_ext(tab,equipe_dom,equipe_ext):
    return force_attaque_ext(tab,equipe_ext) * force_defense_dom(tab,equipe_dom) * nombre_moyen_but_ligue_ext(tab)

def proba_gagnant(tab,equipe_dom,equipe_ext):
    L1=[]
    L2=[]
    lambda1 = lambda_dom(tab,equipe_dom,equipe_ext)
    lambda2 = lambda_ext(tab,equipe_dom,equipe_ext)
    for k in range(10):
        #loi de Poisson 
        L1.append( exp(-lambda1) * ((lambda1)**k) / factorial(k) )
        L2.append( exp(-lambda2) * ((lambda2)**k) / factorial(k) ) 
    prob_dom_gagne=0
    prob_ext_gagne=0
    for k in range(1,10):
        for l in range(k-1):
            prob_dom_gagne += L1[k] * L2[l]
            prob_ext_gagne += L1[l] * L2[k]
    prob_egalite = 1-(prob_ext_gagne+prob_dom_gagne)
    
    # Afficage des probas simplifié : 
    p1 = int( 1000 * prob_dom_gagne ) /10
    pe = int( 1000 * prob_egalite ) /10
    p2 = int( 1000 * prob_ext_gagne ) /10
#    p1 =  prob_dom_gagne 
#    pe =  prob_egalite
#    p2 =  prob_ext_gagne 
#       
    if prob_egalite > prob_dom_gagne and prob_egalite > prob_ext_gagne:
        # Cas d'egalite 
        return equipe_dom,'vs',equipe_ext,'Egalité', p1, pe, p2
    if prob_ext_gagne > prob_dom_gagne : 
        # Equipe à l'extérieur gagne
        return equipe_dom,'vs',equipe_ext, equipe_ext, 'gagne', p1, pe, p2
    if prob_ext_gagne < prob_dom_gagne:
        # Equipe à domicile gagne
        return equipe_dom,'vs',equipe_ext,equipe_dom, 'gagne', p1, pe, p2
    

teams = get_teams_list(tab)



def Test_prediction(tab):
    
    total_match_count = tab['FTHG'].shape[0]
    S = 0
    l=[]
    for i in range(total_match_count):
        # On enregistre le résultat de chaque match 
        if tab['FTHG'][i]>tab['FTAG'][i]:
            res = tab['HomeTeam'][i],'gagne'
        if tab['FTHG'][i]<tab['FTAG'][i]:
            res = tab['AwayTeam'][i],'gagne'
        else:
            res = 'Egalité','oo'
        # On prévoit le résultat du match 
        p = proba_gagnant(tab,tab['HomeTeam'][i],tab['AwayTeam'][i])
        l.append([p[0],res[0]])
        
        if p[0] == res[0] : 
            S+=1
    
    resultat_prediction = S/(total_match_count) * 100
    
    return resultat_prediction
    



#print(calcul_nb_but_dom(tab , 'Man City'))
#
#print(lambda_dom(tab,'Bournemouth','Man City'))
#print(lambda_ext(tab,'Bournemouth','Man City'))
#
#print(proba_gagnant(tab,'Arsenal','Liverpool'))
#print(proba_gagnant(tab,'Arsenal','Man City'))
#
#print(Test_prediction(tab))
#print(Test_prediction(tab2018))
#
#print(Test_prediction(tab2017and2018))

print(proba_gagnant(tab2018,'Chelsea','Man United'))

"""

Prévision des matchs du week_end

"""


def matchs_we(tab,calendrier,date):
    
    total_match_count = calendrier['HOME TEAM'].shape[0]
    
    l=[]
    
    for i in range(total_match_count):
        if calendrier['DATE'][i] == date:
            l.append([calendrier['HOME TEAM'][i],calendrier['AWAY TEAM'][i]])
    return l

week_end = ['2018-10-20 00:00:00','2018-10-21 00:00:00','2018-10-22 00:00:00']


d1 = datetime(2018, 11, 10, 0, 0)
d2 = datetime(2018, 11, 11, 0, 0)
d3 = datetime(2018, 11, 22, 0, 0)

d = [d1,d2]

l=[]
for j in range(len(d)):
    l += matchs_we(tab2018,calendrier_PL2018,d[j])
#print(l)

matchs_we1 = []
for j in range(len(l)):
    if l[j][0]== 'Wolverhampton Wanderers' or l[j][1]== 'Wolverhampton Wanderers' or l[j][0]=='Fulham' or l[j][1]== 'Fulham':                       
        pass
    else:  
        matchs_we1.append(proba_gagnant(tab2018,l[j][0],l[j][1]))

print(matchs_we1)

#print(calendrier_PL2018['DATE'])


#total_match_count = calendrier_PL2018['HOME TEAM'].shape[0]
#
#date = '2018-10-20 00:00:00'
#    
#for i in range(total_match_count):
#    if calendrier_PL2018['DATE'][i] == date:
#        print(date)
#    print(calendrier_PL2018['DATE'][i])
        




""" 

Correspondance des tableaux Excel pour l'ecriture des équipes  
  
"""
## code V1.2

equipesres = ['Man City','Tottenham','Man United','Leicester','Wolves','Brighton','West Ham','Newcastle','Huddersfield','Cardiff']
equipescal = ['Manchester City','Tottenham Hotspur','Manchester United','Leicester City','Wolverhampton Wanderers','Brighton and Hove Albion','West Ham United','Newcastle United','Huddersfield Town','Cardiff City']                     

def changement_nom_equipes(tab,equipescal,equiperes):
    
    
    for i in range(380):
        for j in range(len(equipesres)):
            if calendrier_PL2018['HOME TEAM'][i]==equipescal[j]:
                calendrier_PL2018['HOME TEAM'][i]=equipesres[j]
            
            if calendrier_PL2018['AWAY TEAM'][i]==equipescal[j]:
                calendrier_PL2018['AWAY TEAM'][i]=equipesres[j]
                
    return 'Equipes Changées'

        
            
        










