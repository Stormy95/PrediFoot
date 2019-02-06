import T00_cons
from T03_tf_chris import NeuralNet,normalise_features_per_fifa

import numpy as np
import matplotlib.pyplot as plt

def load_np_odds_result(league,seasonTB):
    path = './data/' + league + '/vectors/'
    odds_file = path + 'out_odds_season_' + str(seasonTB) + '.txt'
    result_file = path + 'out_result3_season_' + str(seasonTB) + '.txt'

    try:
        odds = np.loadtxt(odds_file, dtype=float)
        result = np.loadtxt(result_file, dtype=float)
    except:
        print("Error loading odds and real files for season %i!" %seasonTB)
        print("ABORTED!")
        quit()

    return odds,result

def predict_season(league,seasonTB):
    path = './data/' + league + '/vectors/'
    input_file = path + 'in_season_' + str(seasonTB) + '.txt'

    # Load variables
    try:
        inputs = np.apply_along_axis(normalise_features_per_fifa, 0, np.loadtxt(input_file, dtype=float))
    except:
        print("ERROR loading inputs for season %i" %seasonTB)
        print("ABORTED")
        quit()

    # Set NN
    net = NeuralNet()

    # Path NN
    path_model = './data/' + league + '/model/'
    m_name = path_model + 'TF_chris'

    # Predict
    predict = net.predict(inputs, model_name= m_name)
    return predict

def transform_predict_5to3(predict):
    n_matches = np.size(predict,0)
    new_predict = np.zeros((n_matches,3))

    for n in range(n_matches):
        home = predict[n][0] + predict[n][1]
        draw = predict[n][2]
        away =  predict[n][3] + predict[n][4]

        new_predict[n][0] = home
        new_predict[n][1] = draw
        new_predict[n][2] = away

    return new_predict

def reussite_testback(predict,result):
    good = [0,0,0]
    n_matches = len(result)
    for n in range(0,n_matches):
        # Outcome index
        max_r = np.argmax(result[n])

        # Index of predicted outcome
        first_p = np.argsort(predict[n])[2]
        second_p = np.argsort(predict[n])[1]
        third_p = np.argsort(predict[n])[0]

        # To check how many times the first probability was predicted by the model
        # aswell as the second and third
        # good[0] -> first p , good[1] -> second p , good[2] -> third p

        if max_r == first_p:
            good[0] += 1
        elif max_r == second_p:
            good[1] += 1
        elif max_r == third_p:
            good[2] += 1
        else:
            print('ERROR! Check predict, Maybe it is not in [1 0 0] form')
            quit()

        g_0 = good[0]
        g_1 = good[1]
        g_2 = good[2]

        print(n,'   ',predict[n][:],first_p,'    ',max_r,result[n][:],g_0,g_1,g_2)

def bet_season(predict,odds,result):
    # Maximum odds to bet
    # Equiprobabilistic: p = 1/3
    odds_max = 3

    #
    p_min = 0.25
    esp_min = 0*(1/100)

    bank = 100
    count = 0
    count_goodbets = 0

    ### Betting
    max_bet = 15
    min_bet = 1

    ### Banks
    # Real
    bank_real = []
    bank_real.append(bank)
    # Expected value
    bank_e_v = []
    bank_e_v.append(bank)
    # Expected growth
    bank_e_g = []
    bank_e_g.append(bank)

    betted_matches = []

    n_matches = len(result)
    for n in range(0,n_matches):
        place_bet = 0

        # To get the winner (outcome)
        max_r = np.argmax(result[n])

        # Index of predicted outcome
        first_p = np.argsort(predict[n])[2]
        second_p = np.argsort(predict[n])[1]
        third_p = np.argsort(predict[n])[0]

        # How much you should bet
        f = bet_crit(predict[n],odds[n])

        # Esperance of bets
        e_v,e_g = expected(f,predict[n],odds[n])

        index_ev = np.argsort(e_v)[2]
        index_eg = np.argsort(e_g)[2]

        bet_index = index_ev

        if (e_v[bet_index] > esp_min and
           odds[n][bet_index] < odds_max and
           predict[n][bet_index] > p_min):

            count += 1

            max_bet = 0.15*bank

            bet = np.clip(f[bet_index]*bank,min_bet,max_bet)
            betted_matches.append(n)

            bank_ev = bank*(1+e_v[bet_index])
            bank_e_v.append(bank_ev)

            bank_eg = bank*(e_g[bet_index])
            bank_e_g.append(bank_eg)

            if bet_index == max_r:
                bank += (odds[n][bet_index]-1)*bet
                count_goodbets += 1
            else:
                bank -= bet

            bank_real.append(bank)

    xis = np.arange(len(bank_real))
    print('Bets/Goods/Percen:',count,count_goodbets,count_goodbets/count)
    print('Betted matches:',betted_matches)
    print('-------------------------------')
    print(xis,bank_real)
    # plt.plot(xis,bank_real)
    plt.plot(xis,bank_real)
    plt.show()

def whatsoever(league,seasonTB):
    odds, result = load_np_odds_result(league,seasonTB)
    predict = predict_season(league,seasonTB)
    #predict = transform_predict_5to3(predict)
    reussite_testback(predict,result)
    bet_season(predict,odds,result)

def bet_crit(prob,odds):
    # p : event happens
    # q : not happen
    p = prob
    q = 1-p

    # b : net winnings
    b = odds-1

    # Kelly crit
    f = (b*p - q)/b
    indexes = np.where(f<0)
    for index in indexes:
        f[index] = 0

    return f

def expected(f,prob,odds):
    # f : portion of bank

    # p : event happens
    # q : not happen
    p = prob
    q = 1-p

    b = odds-1

    # e_v : expected value
    # B/B0 : bank
    # B = B0 + e_v
    e_v = b*f*p - f*q

    # e_g : expected growth
    # B/B0 : bank
    # B = B0 * e_g
    e_g = ((1+b*f)**p)*((1-f)**q)-1

    return e_v,e_g

##################################################################

league = T00_cons.league
seasonTB = T00_cons.seasonTB

##################################################################

whatsoever(league,seasonTB)
