import csv
import pandas as pd


# calcPassing is a function that will calculate fantasy points (ppr) based on passing stats.
# calcPassing requires an array with player stats in the following format:
# [Player,PID,Pos,Week,Tm,Cmp,Att,PassYds,PassTD,Int,Sacked,YardsLostSack,PassLng,Rate,Att,RushYards,RushTD,RushLng,
# Tgt,Rec,RecYds,RecTD,RecLng,Fmb,FL,Snap,Snap%]
def calcPassing(playerStats):
    passingPoints = 0
    # Calc passing yards
    # print(playerStats)
    passingPoints += float(playerStats[8]) * 0.04
    # Calc passing tds
    passingPoints += float(playerStats[9]) * 4
    # Calc ints
    passingPoints += float(playerStats[10]) * -1
    # Check for 300 yard pass game
    if float(playerStats[8]) > 300:
        passingPoints += 3
    # Round points to two decimal places
    passingPoints = round(passingPoints, 2)
    return passingPoints


# calcRushing is a function that will calculate fantasy points (ppr) based on rushing stats.
# calcRushing requires an array with player stats in the following format:
# [Player,PID,Pos,Week,Tm,Cmp,Att,PassYds,PassTD,Int,Sacked,YardsLostSack,PassLng,Rate,Att,RushYards,RushTD,RushLng,
# Tgt,Rec,RecYds,RecTD,RecLng,Fmb,FL,Snap,Snap%]
def calcRushing(playerStats):
    rushingPoints = 0
    # Calc rush yards
    rushingPoints += float(playerStats[16]) * 0.1
    # Calc rush tds
    rushingPoints += float(playerStats[17]) * 6
    # Check for 100 yard rush game
    if float(playerStats[16]) > 100:
        rushingPoints += 3
    # Round points to two decimal places
    rushingPoints = round(rushingPoints, 2)
    return rushingPoints


# calcReceiving is a function that will calculate fantasy points (ppr) based on receiving stats.
# calcReceiving requires an array with player stats in the following format:
# [Player,PID,Pos,Week,Tm,Cmp,Att,PassYds,PassTD,Int,Sacked,YardsLostSack,PassLng,Rate,Att,RushYards,RushTD,RushLng,
# Tgt,Rec,RecYds,RecTD,RecLng,Fmb,FL,Snap,Snap%]
def calcReceiving(playerStats):
    receivingPoints = 0
    # Calc receptions
    receivingPoints += float(playerStats[20]) * 1
    # Calc receiving yards
    receivingPoints += float(playerStats[21]) * 0.1
    # Calc receiving tds
    receivingPoints += float(playerStats[22]) * 6
    # Check for 100 yard receiving game
    if float(playerStats[21]) > 100:
        receivingPoints += 3
    # Subtract 1 for fumbles lost (this is done for all players, so it doesn't really need to be in this function it
    #  can be in any of the functions)
    receivingPoints += float(playerStats[25]) * -1
    # Round points to two decimal places
    receivingPoints = round(receivingPoints, 2)
    return receivingPoints


# getNamesAndFp takes a dataframe of players and will calculate the fp for them.
# It returns a DF with the following columns [PlayerName, Pos, Week, Tm, Fpts]
def getNamesAndFp(dataframe):
    output = []
    dataframe = dataframe.values.tolist()

    for row in dataframe:
        # Calculate and append PPR fantasy points to the end of the current player array
        pprFantasyPoints = round(calcPassing(row) + calcRushing(row) + calcReceiving(row), 2)
        output.append([row[0], row[2], row[3], row[4], pprFantasyPoints])
    outputDf = pd.DataFrame(output, columns=['Player', 'Pos', 'Week', 'Tm', 'Fpts'])

    return outputDf


def main():
    pass
    # # Open the file and calculate fantasy points
    # path = "Week 8.csv"
    # # Read in Data
    # rows = []
    # with open(path, newline='') as csvfile:
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         rows.append(row)
    # # Edit the Data
    # for i in range(1, len(rows)):
    #     # print(rows[i])
    #     # print(calcPassing(rows[i]))
    #     # print(calcRushing(rows[i]))
    #     # print(calcReceiving(rows[i]))
    #     # print(calcPassing(rows[i]) + calcRushing(rows[i]) + calcReceiving(rows[i]))
    #     # Calculate and append PPR fantasy points to the end of the current player array
    #     pprFantasyPoints = calcPassing(rows[i]) + calcRushing(rows[i]) + calcReceiving(rows[i])
    #     rows[i].append(pprFantasyPoints)
    #
    # # Write the new Data to File
    # with open(path, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(rows)
    # allPlayerData = pd.read_csv('Weeks 1-7 (2).csv')
    # print(getNamesAndFp(allPlayerData))
    # test = getNamesAndFp(allPlayerData)
    #
    #
    # print(test)


if __name__ == "__main__":
    main()
