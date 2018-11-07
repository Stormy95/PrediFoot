import matplotlib.pyplot as plt
import json
from slugify import slugify

def ChangeMonth(DateStr):
    In = DateStr

    if "January" in DateStr:
        Out = DateStr.replace("January","01")
    elif "February" in DateStr:
        Out = DateStr.replace("February","02")
    elif "March" in DateStr:
        Out = DateStr.replace("March","03")
    elif "April" in DateStr:
        Out = DateStr.replace("April","04")
    elif "May" in DateStr:
        Out = DateStr.replace("May","05")
    elif "August" in DateStr:
        Out = DateStr.replace("August","08")
    elif "September" in DateStr:
        Out = DateStr.replace("September","09")
    elif "October" in DateStr:
        Out = DateStr.replace("October","10")
    elif "November" in DateStr:
        Out = DateStr.replace("November","11")
    elif "December" in DateStr:
        Out = DateStr.replace("December","12")

    return Out

def SortDates(Matches):
    unordered = []
    for match in Matches:
        match["info"]["date"] = slugify(ChangeMonth(match["info"]["date"]))
        unordered.append(match["info"]["date"])

    lowest = unordered[0][3:5]
    ordered = []
    i = 0

    while len(unordered) > 0:
        if  int(unordered[i][3:5]) < int(lowest):
            lowest = unordered[i][3:5]
        i += 1
        if i == len(unordered):
            ordered.append(lowest)
            unordered.remove(lowest)
            if unordered:
              lowest = unordered[0]
              i = 0

def SimMatch(TeamHome,TeamAway):
    R = 'D'
    return R

def Graph():
    filename = 's16.json'
    with open(filename) as json_file: # Colocar os dados em outra pasta
        Matches = json.load(json_file)

    Nmatches = len(Matches)
    Nround = int(Nmatches/10)
    if int(Nround)-(Nmatches/10) != 0:
        print("\n")
        print("Error! Number of matches not a multiple of 10, round is not finished")
        quit()

    Names = []
    for match in Matches:
        name = match["info"]["home team"]
        if len(Names) == 0:
            Names.append(name)
        else:
            if name not in Names:
                Names.append(name)

    Points = {key: [0]*(Nround+1) for key in Names}
    for n in range(1,Nround+1):
        # 0 ~ 9   10 ~ 19  ...  370 ~ 379
        # n -> 1,38
        for match in Matches[10*n-10:10*n]:
            TeamHome = match["info"]["home team"]
            TeamAway = match["info"]["away team"]
            RMatch = SimMatch(TeamHome,TeamAway)

            if n == 5 :
                if TeamHome == "chelsea":
                    print('oi')
                elif TeamAway == "chelsea":
                    print('oi')

            if RMatch == 'H':
                Points[TeamHome][n] = Points[TeamHome][n-1] + 3
                Points[TeamAway][n] = Points[TeamAway][n-1]
            elif RMatch == 'D':
                Points[TeamHome][n] = Points[TeamHome][n-1] + 1
                Points[TeamAway][n] = Points[TeamAway][n-1] + 1
            elif RMatch == 'A':
                Points[TeamHome][n] = Points[TeamHome][n-1]
                Points[TeamAway][n] = Points[TeamAway][n-1] + 3

        #print(n,Points["chelsea"][n])
    n = 38

    print(Matches[10*n-10:10*n])
    #for TeamNames in Names:
    xplot = [i for i in range(Nround+1)]
    yplot = [0]*(Nround+1)

    for n in range(len(xplot)):
        yplot[n] = Points["chelsea"][n]
        plt.plot(xplot, yplot)
    #plt.show()

#Graph()
#SortDates()
