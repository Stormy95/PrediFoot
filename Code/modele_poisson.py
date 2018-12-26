import pandas as pd
from math import *
import numpy as np
import random
from datetime import *
from datetime import datetime


def calcul_nb_but_dom(tab , equipe):
    """ Calcul nombre de but total de l'equipe home marqués à domicile durant la saison """
    home_goals = tab.loc[tab['HomeTeam']== equipe]['FTHG'].sum()
    return home_goals


def calcul_nb_but_ext(tab,equipe):
    """ Calcul nombre de but total de l'equipe 'équipe' marqués à l'extérieur durant la saison """
    away_goals = tab.loc[tab['AwayTeam']==equipe]['FTAG'].sum()
    return away_goals


def potentiel_attaque_dom(tab,equipe):
    """ Le potentiel d'attaque de l'équipe 'equipe' à domicile """
    home_match_count = tab.loc[tab['HomeTeam']==equipe].shape[0]
    
    #print('Nb buts marqué à domicile : {}, home_match_count : {}, Equipe : {}'.format(calcul_nb_but_dom(tab,equipe), home_match_count, equipe))
    return calcul_nb_but_dom(tab,equipe)/home_match_count


def potentiel_attaque_ext(tab,equipe):
    """ Le potentiel d'attaque de l'équipe 'equipe' à l'extérieur """
    away_match_count = tab.loc[tab['AwayTeam']==equipe].shape[0]
    return calcul_nb_but_ext(tab,equipe)/away_match_count


def calcul_nb_but_pris_dom(tab,equipe):
    """ calcul du nombre de but pris à domicile par l'équipe 'equipe' """
    home_goals_taken = tab.loc[tab['HomeTeam']== equipe]['FTAG'].sum()
    return home_goals_taken


def calcul_nb_but_pris_ext(tab,equipe):
    """ calcul du nombre de but pris à l'extérieur par l'équipe 'equipe' """
    away_goals_taken = tab.loc[tab['AwayTeam']== equipe]['FTHG'].sum()
    return away_goals_taken


def potentiel_defense_dom(tab,equipe):
    """ Le potentiel de défense de l'équipe 'equipe' à domicile """
    home_match_count = tab.loc[tab['HomeTeam']==equipe].shape[0]
    return calcul_nb_but_pris_dom(tab,equipe)/home_match_count


def potentiel_defense_ext(tab,equipe):
    """ Le potentiel de défense de l'équipe 'equipe' à l'extérieur """
    away_match_count = tab.loc[tab['AwayTeam']==equipe].shape[0]
    return calcul_nb_but_pris_ext(tab,equipe)/away_match_count


def nombre_moyen_but_ligue_dom(tab):
    """ Calcul nombre de but total marqués à domicile durant la saison """
    total_home_goals = tab['FTHG'].sum() 
    total_match_count = tab['FTHG'].shape[0]
    
    return total_home_goals / total_match_count


def nombre_moyen_but_ligue_ext(tab):
    """ Calcul nombre de but total marqués à l'extérieur durant la saison """
    total_away_goals = tab['FTAG'].sum() 
    total_match_count = tab['FTAG'].shape[0]
    
    return total_away_goals / total_match_count

# calcul des forces d'attaque et de défense pour l'équipe 'equipe' 
# à domicile ou exterieur 
    
def force_attaque_dom(tab,equipe):
    #print('Potentiel attaque : {}'.format(potentiel_attaque_dom(tab,equipe)))
    return  potentiel_attaque_dom(tab,equipe) / nombre_moyen_but_ligue_dom(tab)
    
def force_attaque_ext(tab,equipe):
    return  potentiel_attaque_ext(tab,equipe) / nombre_moyen_but_ligue_ext(tab)

def force_defense_dom(tab,equipe):
    return  potentiel_defense_dom(tab,equipe) / nombre_moyen_but_ligue_ext(tab) 

def force_defense_ext(tab,equipe):
    return  potentiel_defense_ext(tab,equipe) / nombre_moyen_but_ligue_dom(tab)


# --------- Parametre lambda de la loi de poisson ----------  

def lambda_dom(tab,equipe_dom,equipe_ext):
    #print("Force attaque : {}, force defense : {}, nombre_moyen_buts : {}".format(force_attaque_dom(tab,equipe_dom), force_defense_ext(tab,equipe_ext), nombre_moyen_but_ligue_dom(tab)))
    return force_attaque_dom(tab,equipe_dom) * force_defense_ext(tab,equipe_ext) * nombre_moyen_but_ligue_dom(tab)

def lambda_ext(tab,equipe_dom,equipe_ext):
    return force_attaque_ext(tab,equipe_ext) * force_defense_dom(tab,equipe_dom) * nombre_moyen_but_ligue_ext(tab)

def lambda_dom_pondere(tab,equipe_dom,equipe_ext, ponderation=0.1):
    """ Pondère la valeur du lambda suivant le résultat du dernier match joué 
    entre les 2 équipes """
    
    match_precedent = tab.loc[(tab['HomeTeam']== equipe_ext) & (tab['AwayTeam']==equipe_dom)]
    lam_equipe_dom = lambda_dom(tab, equipe_dom, equipe_ext)
    
    if not match_precedent.empty:
        if (match_precedent['FTHG'] > match_precedent['FTAG']).bool():
            lam_equipe_dom *= 1 - ponderation
        elif (match_precedent['FTHG'] < match_precedent['FTAG']).bool():
            lam_equipe_dom *= 1 + ponderation

    return lam_equipe_dom

def lambda_ext_pondere(tab,equipe_dom,equipe_ext, ponderation=0.1):
    """ Pondère la valeur du lambda suivant le résultat du dernier match joué 
    entre les 2 équipes """
    
    match_precedent = tab.loc[(tab['HomeTeam']== equipe_ext) & (tab['AwayTeam']==equipe_dom)]
    lam_equipe_ext = lambda_ext(tab, equipe_dom, equipe_ext)
    
    if not match_precedent.empty:
        if (match_precedent['FTHG'] > match_precedent['FTAG']).bool():
            lam_equipe_ext *= 1 + ponderation

        elif (match_precedent['FTHG'] < match_precedent['FTAG']).bool():
            lam_equipe_ext *= 1 - ponderation

    return lam_equipe_ext
    
    
def proba_gagnant(tab,equipe_dom,equipe_ext):
    """ Pour un match donné entre equipe_dom et equipe_ext, retourne le 
    résultat du match et les probabilité de chaque possibilité (1,N,2)"""

    L1=[]
    L2=[]
    
    # Calcul des lambdas
    lambda1 = lambda_dom_pondere(tab,equipe_dom,equipe_ext, 0.1)
    lambda2 = lambda_ext_pondere(tab,equipe_dom,equipe_ext, 0.1)
    
    #print('Lambda1 : {}, Lambda2 : {}'.format(lambda1, lambda2))
    
    for k in range(10):
        # Loi de Poisson 
        L1.append( exp(-lambda1) * ((lambda1)**k) / factorial(k) )
        L2.append( exp(-lambda2) * ((lambda2)**k) / factorial(k) ) 
        
    prob_dom_gagne=0
    prob_ext_gagne=0
    
    #print('L1 : {}, L2 : {} \n'.format(L1, L2))
        
    for k in range(1,10):
        for l in range(k-1):
            prob_dom_gagne += L1[k] * L2[l]
            prob_ext_gagne += L1[l] * L2[k]
            
    prob_egalite = 1-(prob_ext_gagne+prob_dom_gagne)
    
    # Afficage des probas simplifié : 
    p1 = int( 1000 * prob_dom_gagne ) /10
    pe = int( 1000 * prob_egalite ) /10
    p2 = int( 1000 * prob_ext_gagne ) /10
    
       
    if prob_egalite > prob_dom_gagne and prob_egalite > prob_ext_gagne:
        # Cas d'egalite 
        return 'Egalité'
    if prob_ext_gagne > prob_dom_gagne : 
        # Equipe à l'extérieur gagne
        return equipe_ext
    if prob_ext_gagne < prob_dom_gagne:
        # Equipe à domicile gagne
        return equipe_dom
    





