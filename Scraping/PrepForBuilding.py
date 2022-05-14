import pandas as pd
import csv
from math import sqrt
from math import pow

sal_players = []
sal_salaries = []
player_game_stats = []
game_stats = []
game_ids = []

# read in precollected players
with open('players.csv', 'r', newline='\n') as f:
    csv_r = csv.reader(f)
    header = next(csv_r)

    for row in csv_r:
        sal_players.append(row)

#read in pre-collected player salary statistics
with open('player_sals.csv', 'r', newline='\n') as f:
    csv_r = csv.reader(f)
    header = next(csv_r)

    for row in csv_r:
        sal_salaries.append(row)


# read in scraped game-by-game player stats
def read_player_stats(year):
    with open('file'+year+'.csv', 'r', newline='\n', encoding='utf-8') as f:
        csv_r = csv.reader(f)
        header = next(csv_r)

        for row in csv_r:
            player_game_stats.append(row)

# read in scraped game results
def read_game_stats(year):
    with open('results'+year+'.csv', 'r', newline='\n', encoding='utf-8') as f:
        csv_r = csv.reader(f)
        header = next(csv_r)

        for row in csv_r:
            game_stats.append(row)



def app_sals(year, player_game_stats):
    '''
    approximate a missing salary with the min salary
    '''
    min = 100000000000
    for pgs in player_game_stats:
        for s in sal_salaries:
            if s[1] == pgs[1] and s[4] == year:
                pgs.append(s[2])
                pgs.append(str(year))
                if int(s[2]) < min:
                    min = int(s[2])
                break;

    return min


def no_sals(year, min, player_game_stats):
    '''
    Normalize all player salaries to 60 minutes of game time
    '''
    for i in range(0, len(player_game_stats)):
        try:
            player_game_stats[i][9]
        except:
            player_game_stats[i].append(str(min))
            player_game_stats[i].append(str(year))

        #fix minutes players for each player
        try:
            mp = float(player_game_stats[i][2][0:2]) + float(player_game_stats[i][2][3:])/60
        except:
            mp = float(player_game_stats[i][2][0:1]) + float(player_game_stats[i][2][2:]) / 60
        player_game_stats[i].append(mp)

def find_max_sals(GameID, player_game_stats):
    '''
    Find the maximum salary for both teams in a given unique Game ID
    '''
    
    HomeMax = 0
    AwayMax = 0
    for pgs in player_game_stats:
        if pgs[7] == GameID:
            if pgs[8] == 'Home' and int(pgs[9]) > HomeMax:
                HomeMax = int(pgs[9])
            elif int(pgs[9]) > AwayMax:
                AwayMax = int(pgs[9])

    return (HomeMax, AwayMax)


def calc_ave_sal(GameID, player_game_stats):
    '''
    Calculate the average salary for both teams in a given Game ID and variance as well as disper1
    '''
    
    HomeVar = 0.0
    AwayVar = 0.0
    HomeAve = 0.0
    AwayAve = 0.0
    HomeMins = 0.0
    AwayMins = 0.0

    #calculate avesal
    for pgs in player_game_stats:
        #print(pgs)
        if pgs[7] == GameID:
            if pgs[8] == 'Home':
                HomeAve += pgs[11] * float(pgs[9])
                HomeMins += pgs[11]
            else:
                AwayAve += pgs[11] * float(pgs[9])
                AwayMins += pgs[11]

    if HomeMins == 0.0 or AwayMins == 0.0:
        return (0,0,0,0,0,0)

    HomeAve = HomeAve/HomeMins
    AwayAve = AwayAve/AwayMins

    # calculate varsal
    for pgs in player_game_stats:
        if pgs[7] == GameID:
            if pgs[8] == 'Home':
                HomeVar += pow((pgs[11] - HomeAve),2) * float(pgs[9])
                HomeMins += pgs[11]
            else:
                AwayVar += pow((pgs[11] - AwayAve),2) * float(pgs[9])
                AwayMins += pgs[11]

    HomeVar = HomeVar/HomeMins
    AwayVar = AwayVar/AwayMins


    #calculate disper1
    HomeDisper1 = (sqrt(HomeVar))/HomeAve
    AwayDisper1 = (sqrt(AwayVar))/AwayAve

    return (AwayAve, HomeAve, AwayVar, HomeVar, AwayDisper1, HomeDisper1)



def build_total_stats(year, player_game_stats, game_stats):
    '''
    Build the game-by-game salary stats for a given year
    '''

    player_game_stats = [el for el in player_game_stats if el[2][0].isdigit()]
    min = app_sals(year, player_game_stats)
    no_sals(year, min, player_game_stats)

    # go over each game in the season and keep track of the calculated metrics for the game
    for game in game_stats:
        if int(game[3]) > int(game[4]):
            game.append('L')
        else:
            game.append('W')

        maxs = find_max_sals(game[0], player_game_stats)

        game.append(maxs[1])
        game.append(maxs[0])

        aves = calc_ave_sal(game[0], player_game_stats)

        game.append(aves[0])
        game.append(aves[1])
        game.append("{:.22f}".format(float(aves[2])))
        game.append("{:.22f}".format(float(aves[3])))
        game.append("{:.22f}".format(float(aves[4])))
        game.append("{:.22f}".format(float(aves[5])))

    return game_stats



def main1(years):
    '''
    Main control function for the script
    '''
    
    all_games = []

    # calculate stats for each desired year
    for year in years:
        read_player_stats(year)
        read_game_stats(year)
        year_stats = build_total_stats(year, player_game_stats, game_stats)
        all_games.append(year_stats)
        player_game_stats = []
        game_stats = []

    # write the collected data to a file
    with open('C:/Users/senic/OneDrive/Desktop/Masters/FALL_2021/ECO1400/Term_Paper/Data/All_Disper_2011_2018.csv', 'w', newline='\n', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(['GameID', "AwayTeam", "HomeTeam", "AwayScore", "HomeScore", "HomeWin", "AwayMaxSal", 'HomeMaxSal', 'AwayAveSal', 'HomeAveSal', 'AwayVarSal', 'HomeVarSal', 'AwayDisper1', 'HomeDisper1'])
        for r in all_games:
            write.writerows(r)

    return all_games


if __name__ == "__main__":

    years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']

    all_games = main1(years)