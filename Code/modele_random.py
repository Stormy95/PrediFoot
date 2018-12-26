import random

def prediction_random(tab, equipe_dom, equipe_ext):
    tirage = random.randint(0,2)
    if tirage == 0:
        return equipe_dom
    if tirage == 1:
        return equipe_ext
    if tirage == 2:
        return 'Egalité'
        
    
    