import T00_cons
from T00_funcs import check_files,csv_to_list,add_fifa,add_lambda,save_matches_json

import numpy as np
import json
import csv

league = T00_cons.league
seasonI = T00_cons.seasonI
seasonO = T00_cons.seasonO

check_files(league,seasonI,seasonO)

for season in range(seasonI,seasonO+1):
    matches = csv_to_list(league,season)
    matches = add_fifa(matches,league,season)
    matches = add_lambda(matches)

    save_matches_json(league,season,matches)
