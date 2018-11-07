# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 15:52:48 2018

@author: yones
"""

import pandas as pd
import numpy as np

tab = pd.read_excel('E0.xlsx')

def calcul_nb_but_dom(tab , equipe):
    home_goals = tab.loc[tab['HomeTeam']== equipe]['FTHG'].sum()
    return home_goals

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
    new_tab = new_tab.to_frame()
    new_tab.to_excel(writer, index=False)

#write_data_excel(tab)

def nombre_moyen_but_ligue_dom(tab):
    total_home_goals = tab['FTHG'].sum() 
    total_match_count = tab['FTHG'].shape[0]
    
    return total_home_goals / total_match_count

def nombre_moyen_but_ligue_ext(tab):
    total_away_goals = tab['FTHG'].sum() 
    total_match_count = tab['FTHG'].shape[0]
    
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
        L1.append( np.random.poisson(k, lambda1) )
        L2.append( np.random.poisson(k, lambda2) ) 
    prob_dom_gagne=0
    prob_ext_gagne=0
    for k in range(1,10):
        for l in range(k-1):
            prob_dom_gagne += L1[k] * L2[l]
            prob_ext_gagne += L1[l] * L2[k]
    if prob_ext_gagne > prob_dom_gagne : 
        return equipe_ext, 'gagne'
    if prob_ext_gagne < prob_dom_gagne:
        return equipe_dom, 'gagne'

##### test 2

teams=get_teams_list(tab)

## pas vraiment utile donne la liste de tous les coeffs
def betaAdom():
    l=[]
    teams=get_teams_list(tab)
    for x in teams :
        l.append( force_attaque_dom(tab,x) )
    return l

def betaAext():
    l=[]
    teams=get_teams_list(tab)
    for x in teams :
        l.append( force_attaque_ext(tab,x) )
    return l

def betaDdom():
    l=[]
    teams=get_teams_list(tab)
    for x in teams :
        l.append( force_defense_dom(tab,x) )
    return l

def betaDext():
    l=[]
    teams=get_teams_list(tab)
    for x in teams :
        l.append( force_defense_ext(tab,x) )
    return l

## utile
    
def beta_vect(equipe1,equipe2,txt):
    V=np.zeros( (2,1) )
    if (txt == 'dom'):
        V[0]=np.log( force_attaque_dom(tab,equipe1) )
        V[1]=np.log( force_defense_ext(tab,equipe2) )
    
    else:
        V[0]=np.log( force_attaque_ext(tab,equipe1) )
        V[1]=np.log( force_defense_dom(tab,equipe2) )
    return V
    
def lambd(equipe1,equipe2,txt):
    U=np.ones( (1,2) )
    x=np.exp( np.dot( U , beta_vect(equipe1,equipe2,txt) ) )
    y=x[0,0]
    return y

def fact(n):
    if n<2:
        return 1
    else:
        return n*fact(n-1)

def poisson(k,lambd):
    return ( np.exp( - lambd )* lambd**k ) / fact(k)
        
def proba_gagnant_2(equipe1,equipe2,txt):     #txt correspond à équipe 1
    txt2=''
    if txt == 'dom':
        txt2='ext'
        
    else :
        txt2= 'dom'
    
    L1=[]
    L2=[]
    lambda1 = lambd(equipe1,equipe2,txt)
    lambda2 = lambd(equipe2,equipe1, txt2)
    
    for k in range(20):
        L1.append( poisson(k, lambda1)*100 )
        L2.append( poisson(k, lambda2)*100 ) 
        
    prob_1_gagne=0
    prob_2_gagne=0
    
    for k in range(1,20):
        for l in range(k-1):
            prob_1_gagne += L1[k] * L2[l]
            prob_2_gagne += L1[l] * L2[k]
    
    if prob_2_gagne > prob_1_gagne : 
        return equipe2, 'gagne' 
    if prob_2_gagne < prob_1_gagne:
        return equipe1, 'gagne'
   

def Test_prediction_2():
    
    total_match_count = tab['FTHG'].shape[0]
    S = 0
    for i in range(total_match_count):
        # On enregistre le résultat de chaque match 
        if tab['FTHG'][i]>tab['FTAG'][i]:
            res = tab['HomeTeam'][i],'gagne'
        if tab['FTHG'][i]<tab['FTAG'][i]:
            res = tab['AwayTeam'][i],'gagne'
        else:
            res = 'Egalité','oo'
            
        # On prévoit le résultat du match 
        p = proba_gagnant_2(tab['HomeTeam'][i],tab['AwayTeam'][i],'dom')
        
        
        if p == res : 
            S+=1
    
    resultat_prediction = S/(total_match_count) * 100
    
    return resultat_prediction
        

        
    
    