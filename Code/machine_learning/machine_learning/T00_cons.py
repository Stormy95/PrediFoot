# League
league = 'PL'

# Testback Season
seasonTB = 18

# Training seasons for the NN
seasonTI = 18
seasonTO = 18
# Validation season for the NN
seasonV = 18


# Seasons to generate files
seasonI = 14
seasonO = 18

# TEAMS_NAMES_'league'_X is a dict that changes the team name to match
# with those from fifa
# 1 : from matches to fifa
# 2 : from odds to fifa
################### PL #####################

TEAMS_NAMES_PL_1 = {
      'afc-bournemouth': 'bournemouth',
      'arsenal': 'arsenal',
      'aston-villa': 'aston-villa',
      'brighton-hove-albion': 'brighton',
      'burnley': 'burnley',
      'cardiff-city': 'cardiff-city',
      'chelsea': 'chelsea',
      'crystal-palace': 'crystal-palace',
      'everton': 'everton',
      'fulham': 'fulham',
      'huddersfield-town': 'huddersfield',
      'hull-city': 'hull-city',
      'leicester-city': 'leicester-city',
      'liverpool': 'liverpool',
      'manchester-city': 'manchester-city',
      'manchester-united': 'manchester-utd',
      'middlesbrough': 'middlesbrough',
      'newcastle-united': 'newcastle-utd',
      'norwich-city': 'norwich',
      'queens-park-rangers': 'qpr',
      'southampton': 'southampton',
      'stoke-city': 'stoke-city',
      'sunderland': 'sunderland',
      'swansea-city': 'swansea-city',
      'tottenham-hotspur': 'spurs',
      'watford': 'watford',
      'west-bromwich-albion': 'west-brom',
      'west-ham-united': 'west-ham',
      'wolverhampton-wanderers': "wolves",
      }

TEAMS_NAMES_PL_2 = {
      'Bournemouth': 'bournemouth',
      'Arsenal': 'arsenal',
      'Aston Villa': 'aston-villa',
      'Brighton': 'brighton',
      'Burnley': 'burnley',
      'Cardiff': 'cardiff-city',
      'Chelsea': 'chelsea',
      'Crystal Palace': 'crystal-palace',
      'Everton': 'everton',
      'Fulham': 'fulham',
      'Huddersfield': 'huddersfield',
      'Hull': 'hull-city',
      'Leicester': 'leicester-city',
      'Liverpool': 'liverpool',
      'Man City': 'manchester-city',
      'Man United': 'manchester-utd',
      'Middlesbrough': 'middlesbrough',
      'Newcastle': 'newcastle-utd',
      'Norwich': 'norwich',
      'QPR': 'qpr',
      'Southampton': 'southampton',
      'Stoke': 'stoke-city',
      'Sunderland': 'sunderland',
      'Swansea': 'swansea-city',
      'Tottenham': 'spurs',
      'Watford': 'watford',
      'West Brom': 'west-brom',
      'West Ham': 'west-ham',
      'Wolves': "wolves",
      }

############################################

ALL_TEAMS = {
            'PL': [TEAMS_NAMES_PL_1,TEAMS_NAMES_PL_2],
            }
