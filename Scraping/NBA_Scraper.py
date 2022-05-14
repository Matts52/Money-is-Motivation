
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv


def getGameIDs(year, endDate):
    '''
    A function to gather all unique GameID's for a given year and ending data and write them to a file
    '''
    
    url = "" #redacted"

    #account for lockout season
    if year == "2012":
        months = ["december", "january", "february", "march", "april"]
    else:
        months = ["october", "november", "december", "january", "february", "march", "april"]
    header = ["GameID"]
    GameId = []

    #gather all regular season Game ID's for a given season
    for month in months:
        html = urlopen(url + month + ".html")
        soup = BeautifulSoup(html, "html.parser")
        tableGames = soup.find("tbody")
        raw = str(tableGames)

        # utilize the common pattern to discern game ID's
        for i in range(0, len(raw)-1):
            try:
                if raw[i] + raw[i+1] + raw[i+2] + raw[i+3] == 'left':
                    if int(raw[i+15:i+17]) == int(endDate[0:2]) and int(raw[i+17:i+19]) > int(endDate[2:4]):
                        break
                    if raw[i+11] == '2':
                        GameId.append([raw[i+11:i+23]])
            except:
                pass

    with open('file'+year+'.csv', 'w', newline='\n') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(header)
        write.writerows(GameId)


def gameScores(GameID):
    '''
    Get the game scoring outcome from a specified unique Game ID, return in format [ID, HomeTeam, AwayTeam, HomeScore, AwayScore]
    '''

    url = "https://www.basketball-reference.com/boxscores/"+GameID+".html"
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    #query the soup to find the scores
    teams = [(soup.findAll('strong')[i].getText()[1:])[:-1] for i in range(1, 3)]
    scores = [(soup.findAll('div', {'class':'scores'})[i].getText()[1:])[:-1] for i in range(0,2)]

    return [GameID, teams[0], teams[1], scores[0], scores[1]]




def GameScoresForSeason(year):
    '''
    Collect all game scores for a given season
    '''
    
    gScores = []
    counter = 0
    #read in each game ID from the selected season
    with open('C:/Users/senic/OneDrive/Desktop/Masters/FALL_2021/ECO1400/Term_Paper/Data/Games_'+year+'.csv', 'r', newline='\n') as f:
        csv_r = csv.reader(f)
        header = next(csv_r)

        # get the score for the game and track progress
        for row in csv_r:
            gScores.append(gameScores(row[0]))
            counter += 1
            print(str((counter / 1230) * 100)[0:4] + "% done the game scores for " + year)

    # write all of the game results to a file
    with open('C:/Users/senic/OneDrive/Desktop/Masters/FALL_2021/ECO1400/Term_Paper/Data/Games_Results_'+year+'.csv', 'w', newline='\n') as f:
        write = csv.writer(f)
        write.writerow(['GameID', "Away", "Home", "Apts", "Hpts"])
        write.writerows(gScores)


def PlayerStatsByGame(GameID):
    '''
    Collect player stats for a given Game ID, including minutes, points, rebounds, assists, turnovers
    '''
    
    url = "https://www.basketball-reference.com/boxscores/"+GameID+".html"
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    tables = list(soup.findAll('tbody'))

    #0, 8 being key positions for team in the split html
    teams =  [[] for i in range(0,2)]

    switch = 0

    for i in [0, 8, 9]:
        strForm = str(tables[i])
        strSpl = strForm.split('>')

        if i != 0:
            x = 1
            if strSpl[4][:-3] == teams[0][0][0] or switch == 1:
                continue
        else:
            x = 0

        # get starting players
        for j in range(0, 5):
            findUserName = strSpl[2 + (j*46)]
            findUserName = findUserName.split('=')
            findUserName = findUserName[3].split('\"')

            teams[x].append([])
            teams[x][j].append(strSpl[4 + (j*46)][:-3])
            teams[x][j].append(findUserName[1])
            teams[x][j].append(strSpl[7 + (j * 46)][:-4])
            teams[x][j].append(strSpl[31 + (j * 46)][:-4])
            teams[x][j].append(strSpl[33 + (j * 46)][:-4])
            teams[x][j].append(strSpl[39 + (j * 46)][:-4])
            teams[x][j].append(strSpl[43 + (j * 46)][:-4])
            teams[x][j].append(GameID)
            if x == 0: teams[x][j].append('Away')
            else: teams[x][j].append('Home')

        # get reserve players, except for those that didnt play
        for j in range(0, 10):
            try:
                if strSpl[278 + (j * 46) + 3] != 'Did Not Play</td':
                    findUserName = strSpl[276 + (j * 46)]
                    findUserName = findUserName.split('=')
                    findUserName = findUserName[3].split('\"')

                    teams[x].append([])
                    teams[x][j+5].append(strSpl[278 + (j * 46)][:-3])
                    teams[x][j+5].append(findUserName[1])
                    teams[x][j+5].append(strSpl[281 + (j * 46)][:-4])
                    teams[x][j+5].append(strSpl[305 + (j * 46)][:-4])
                    teams[x][j+5].append(strSpl[307 + (j * 46)][:-4])
                    teams[x][j+5].append(strSpl[313 + (j * 46)][:-4])
                    teams[x][j+5].append(strSpl[317 + (j * 46)][:-4])
                    teams[x][j+5].append(GameID)
                    if x == 0: teams[x][j+5].append('Away')
                    else: teams[x][j+5].append('Home')

            except:
                pass

        if i == 8:
            switch = 1

    return teams


def PlayerStatsBySeason(year):
    '''
    Collect the game-by-game player stats for a full selected season and write them to a file
    '''

    PlayerStats = []

    counter = 0
    #read in selected season
    with open('C:/Users/senic/OneDrive/Desktop/Masters/FALL_2021/ECO1400/Term_Paper/Data/Games_' + year + '.csv', 'r', newline='\n') as f:
        csv_r = csv.reader(f)
        header = next(csv_r)

        # get player stats for given game and track progress
        for row in csv_r:
            gameStats = PlayerStatsByGame(row[0])
            PlayerStats.append(gameStats[0])
            PlayerStats.append(gameStats[1])

            counter += 1
            print(str((counter / 1230) * 100)[0:4] + "% done the player stats for " + year)

    # write the player stats for the season to a new file
    with open('C:/Users/senic/OneDrive/Desktop/Masters/FALL_2021/ECO1400/Term_Paper/Data/Player_Game_Stats_'+year+'.csv', 'w', newline='\n', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(['Name', "UName", "MP", "RB", "AS", "TOV", "PTS", 'GameID', 'Team'])
        for r in PlayerStats:
            write.writerows(r)

    return

if __name__ == "__main__":
    # Gather the GameID's for all games between the selected years

    years = ["2014", "2015", "2016", "2017", "2018"]
    endDate = ["0419", "0418", "0413", "0412", "0411"]

    #Gather all of the GameID's
    for i in range(0, len(years)):
        getGameIDs(years[i], endDate[i])

    # Gather Game-By-Game statistics
    for year in years:
        GameScoresForSeason(year)

    # Gather game by game player stats
    for year in years:
        PlayerStatsBySeason(year)



