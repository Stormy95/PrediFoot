import matplotlib.pyplot as plt
import numpy as np

from modele_poisson import *
from modele_random import *
#from modele_classement import *


tab2013 = pd.read_csv('2013_2014.csv')
tab2014 = pd.read_csv('2014_2015.csv')
tab2015 = pd.read_csv('2015_2016.csv')
tab2016 = pd.read_csv('2016_2017.csv')
tab2017 = pd.read_csv('2017_2018.csv')


def test_prediction(tab_training, tab_testing, fonction_prediction, training_size=190):
    
    total_match_count = tab_testing['FTHG'].shape[0]
    S = 0
    l=[]
    for i in range(training_size, training_size+total_match_count):
        # On enregistre le résultat de chaque match 
        if tab_testing['FTHG'][i]>tab_testing['FTAG'][i]:
            res = tab_testing['HomeTeam'][i]
        if tab_testing['FTHG'][i]<tab_testing['FTAG'][i]:
            res = tab_testing['AwayTeam'][i]
        else:
            res = 'Egalité'
        # On prévoit le résultat du match 
        p = fonction_prediction(tab_training,tab_testing['HomeTeam'][i],tab_testing['AwayTeam'][i])
        l.append([p,res])
        
        if p == res : 
            S+=1
    
    resultat_prediction = S/(total_match_count) * 100
    
    return resultat_prediction


def plot_result(training_size=190):

    x = ['2013-2014', '2015-2016', '2016-2017', '2017-2018']
    
    random2013 = test_prediction(tab2013[:training_size], tab2013[training_size:], prediction_random, training_size)
    #random2014 = test_prediction(tab2014, prediction_random)
    random2015 = test_prediction(tab2015[:training_size], tab2015[training_size:], prediction_random, training_size)
    random2016 = test_prediction(tab2016[:training_size], tab2016[training_size:], prediction_random, training_size)
    random2017 = test_prediction(tab2017[:training_size], tab2017[training_size:], prediction_random, training_size)
    
    y_random = [random2013, random2015, random2016, random2017]
    plt.plot(x, y_random, '-o', label='Modèle Aléatoire')
    
    poisson2013 = test_prediction(tab2013[:training_size], tab2013[training_size:], proba_gagnant, training_size)
    #poisson2014 = test_prediction(tab2014, proba_gagnant)
    poisson2015 = test_prediction(tab2015[:training_size], tab2015[training_size:], proba_gagnant, training_size)
    poisson2016 = test_prediction(tab2016[:training_size], tab2016[training_size:], proba_gagnant, training_size)
    poisson2017 = test_prediction(tab2017[:training_size], tab2017[training_size:], proba_gagnant, training_size)
    
    y_poisson = [poisson2013,  poisson2015, poisson2016, poisson2017]
    print(y_poisson)
    

    plt.plot(x, y_poisson, '-o', label='Modèle Poisson')
    
    plt.xlabel('Saisons')
    plt.ylabel('Pourcentage de réussite')
    plt.title('Benchmark')
    plt.legend()
    plt.show()
    


def evolution_taille_training():
    result = []
    l = [47,95,142,190,237,285]
    for training_size in l:
        poisson2015 = test_prediction(tab2015[:training_size], tab2015[training_size:], proba_gagnant, training_size)
        result.append(poisson2015)
        
    plt.xlabel('Nombre de match de training')
    plt.ylabel('Pourcentage de réussite')
    plt.title('Evolution du pourcentage de réussite en fonction du nombre de match de training pour la saison 2015-2016')
    plt.plot(l, result, '-o')
    plt.show()
    

plot_result()
#evolution_taille_training()
