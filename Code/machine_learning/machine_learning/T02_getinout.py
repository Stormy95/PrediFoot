import T00_cons
from T00_funcs import generate_inout,save_inout_txt

import numpy as np
import json
import csv

league = T00_cons.league
seasonI = T00_cons.seasonI
seasonO = T00_cons.seasonO

for season in range(seasonI,seasonO+1):
    list_in,list_out_odds,list_out_result3,list_out_result = generate_inout(league,season)
    save_inout_txt(league,season,list_in,list_out_odds,list_out_result3,list_out_result)
