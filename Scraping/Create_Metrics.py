import pandas as pd
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np

# Create a list of all team codes
team_codes = ['PHI','MIL','CHI','CLE','BOS','LAC','MEM','ATL','MIA','CHO','UTA','SAC','NYK','LAL','ORL','DAL','BRK','DEN','IND','NOP','DET','TOR','HOU','SAS','PHO','OKC','MIN','POR','GSW','WAS']

# Createa dictionary mapping team codes to team names
team_dict = {
'PHI':'Philadelphia 76ers',
'MIL':'Milwaukee Bucks',
'CHI':'Chicago Bulls',
'CLE':'Cleveland Cavaliers',
'BOS':'Boston Celtics',
'LAC':'Los Angeles Clippers',
'MEM':'Memphis Grizzlies',
'ATL':'Atlanta Hawks',
'MIA':'Miami Heat',
'CHO':'Charlotte Hornets',
'UTA':'Utah Jazz',
'SAC':'Sacramento Kings',
'NYK':'New York Knicks',
'LAL':'Los Angeles Lakers',
'ORL':'Orlando Magic',
'DAL':'Dallas Mavericks',
'BRK':'Brooklyn Nets',
'DEN':'Denver Nuggets',
'IND':'Indiana Pacers',
'NOP':'New Orleans Pelicans',
'DET':'Detroit Pistons',
'TOR':'Toronto Raptors',
'HOU':'Houston Rockets',
'SAS':'San Antonio Spurs',
'PHO':'Phoenix Suns',
'OKC':'Oklahoma City Thunder',
'MIN':'Minnesota Timberwolves',
'POR':'Portland Trail Blazers',
'GSW':'Golden State Warriors',
'WAS':'Washington Wizards',
'NJN':'New Jersey Nets',
'NOH':'New Orleans Hornets',
'CHA':'Charlotte Bobcats'
}


sal_salaries = []
game_stats = []

# Begin Script

# read in the pre-collected NBA salary data
with open('file_sals.csv', 'r', newline='\n') as f:
    csv_r = csv.reader(f)
    header = next(csv_r)

    for row in csv_r:
        sal_salaries.append(row)

# read in the built file from PrepForBuilding.py 
with open('file_built.csv', 'r', newline='\n', encoding='utf-8') as f:
    csv_r = csv.reader(f)
    header = next(csv_r)

    for row in csv_r:
        game_stats.append(row)



def PlayerStatsByYear(team, year):
    '''
    Scrape the year level player statistics for a given team
    '''
    
    url = '' #redacted 
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    team_stats = []
    tables = list(soup.findAll('table', {'id':'per_game'}))
    rows = iter(tables[0].find_all('tr'))
    counter = 1

    # for each player on the team, gather their stats and append that content to a table 
    for row in rows:
        if counter == 1:
            counter = 0
            continue
        else:
            player_code = str(row.find('td', {'data-stat':'player'}).contents[0])[20:29]
            player = row.find('td', {'data-stat':'player'}).contents[0].contents[0]
            games = row.find('td', {'data-stat': 'g'}).contents[0].contents[0]

            found = 0
            for p in sal_salaries:
                if p[1] == player_code:
                    sal = p[2]
                    found = 1
            if found == 0:
                continue

            team_stats.append([team, year, player, games, player_code, sal])


    return team_stats




def Disper2_Teams(all_players):
    '''
    Calcualte disper2 for a given team
    '''
    
    all_disp = []
    rel_players = []

    for year in ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']:
        for code in team_codes:
            # special case team codes
            if code == 'BRK' and year in ('2011', '2012'): code = 'NJN'
            elif code == 'NOP' and year in ('2011', '2012', '2013'): code = 'NOH'
            elif code == 'CHO' and year in ('2011', '2012', '2013', '2014'): code = 'CHA'
            for t in all_players:
                for p in t:
                    if p[0] == code and p[1] == year:
                        rel_players.append(float(p[5]))
                        
            arr = np.array(rel_players)
            GC = gini_coefficient(arr)
            all_disp.append([year, code, GC])
            arr = None
            rel_players = []

    return all_disp



def gini_coefficient(x):
    """Compute Gini coefficient of array of values"""
    diffsum = 0
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))
    return diffsum / (len(x)**2 * np.mean(x))

def hhi(series):
    sumS = sum(series)
    weights = []
    for item in series:
        weights.append((item/sumS)*100)
    HHI = 0
    for w in weights:
        HHI += w**2

    return HHI


def Disper3_Teams(all_players):
    '''
    Calcualte disper3 for a given team
    '''
    all_disp = []
    rel_players = []

    for year in ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']:
        for code in team_codes:
            # special case team codes
            if code == 'BRK' and year in ('2011', '2012'): code = 'NJN'
            elif code == 'NOP' and year in ('2011', '2012', '2013'): code = 'NOH'
            elif code == 'CHO' and year in ('2011', '2012', '2013', '2014'): code = 'CHA'
            for t in all_players:
                for p in t:
                    if p[0] == code and p[1] == year and int(p[3]) >= 42:
                        rel_players.append(float(p[5]))
                    elif p[0] == code and p[1] == '2012' and int(p[3]) >= 33:
                        rel_players.append(float(p[5]))
            #arr = np.array(rel_players)
            HI = hhi(rel_players)
            all_disp.append([year, code, HI])
            arr = None
            rel_players = []

    return all_disp





if __name__ == '__main__':
    years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']

    all_players = []

    for year in years:
        for code in team_codes:
            if code == 'BRK' and year in ('2011', '2012'): code = 'NJN'
            elif code == 'NOP' and year in ('2011', '2012', '2013'): code = 'NOH'
            elif code == 'CHO' and year in ('2011', '2012', '2013', '2014'): code = 'CHA'
            tempTeam = PlayerStatsByYear(code, year)
            all_players.append(tempTeam)


    all_disp2 = Disper2_Teams(all_players)
    all_disp3 = Disper3_Teams(all_players)

    new_games = []
    temp_game = []

    #for each game
    for g in game_stats:

        year = g[0][0:4]

        temp_game = g.copy()

        counter = 0
        countHelp = ''

        #update disp 2 for both teams
        for d in all_disp2:
            #awayteam
            if (int(d[0]) - 1 == int(year) and int(g[0][4:6]) > 6) and team_dict[d[1]] == g[1]:
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break
            elif int(g[0][4:6]) < 6 and d[0] == year and team_dict[d[1]] == g[1]:
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break
        for d in all_disp2:
            #hometeam
            if (int(d[0]) - 1 == int(year) and int(g[0][4:6]) > 6) and team_dict[d[1]] == g[2]:
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break
            elif int(g[0][4:6]) < 6 and d[0] == year and team_dict[d[1]] == g[2]:
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break

        #update disp 3 for both teams
        for d in all_disp3:
            #awayteam
            if (int(d[0]) - 1 == int(year) and int(g[0][4:6]) > 6) and team_dict[d[1]] == g[1]:
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break
            elif int(g[0][4:6]) < 6 and d[0] == year and team_dict[d[1]] == g[1]:
            #hometeam
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break


        for d in all_disp3:
            if (int(d[0]) - 1 == int(year) and int(g[0][4:6]) > 6) and team_dict[d[1]] == g[2]:
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break
            elif int(g[0][4:6]) < 6 and d[0] == year and team_dict[d[1]] == g[2]:
                temp_game.append("{:.22f}".format(float(d[2])))
                counter += 1
                countHelp += '3'
                break

        if counter != 4:
            print(g)
            print(countHelp)
            raise Exception('Bad Try')

        if g[5] == 'W':
            temp_game.append(1)
        else:
            temp_game.append(0)

        new_games.append(temp_game.copy())
        temp_game = []

    print(new_games[0])

    with open('file_ready_for_R.csv', 'w', newline='\n', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(['GameID', "AwayTeam", "HomeTeam", "AwayScore", "HomeScore", "HomeWin", "AwayMaxSal", 'HomeMaxSal', 'AwayAveSal', 'HomeAveSal', 'AwayVarSal', 'HomeVarSal', 'AwayDisper1', 'HomeDisper1', 'AwayDisper2', 'HomeDisper2', 'AwayDisper3', 'HomeDisper3', 'HomeWinBinary'])
        for r in new_games:
            write.writerow(r)


