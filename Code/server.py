""" Serveur du site web situé à l'adresse : http://srawls35.pythonanywhere.com/ """


from flask import *
from modele_poisson import *
import pandas as pd

app = Flask(__name__)

FLASK_DEBUG=1

@app.route('/', methods=['GET', 'POST'])
def accueil():

    #tab2017 = pd.read_csv(url_for('static', filename='2017_2018.csv'))
    tab2017 = pd.read_csv('2017_2018.csv')
    team_list = list(tab2017['HomeTeam'].drop_duplicates())
    
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        prediction = proba_gagnant(tab2017,team1, team2)
        return render_template('index.html', team_list = team_list, prediction="Résultat : {}".format(prediction))
    else:
        return render_template('index.html', team_list = team_list, prediction="")

if __name__ == '__main__':
    app.run(debug=True)
