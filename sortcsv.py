from sklearn import metrics
from sklearn.linear_model import LinearRegression, PoissonRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import pandas as pd

allPlayerData = pd.read_csv('Weeks 1-7.csv')
wrData = allPlayerData.loc[(allPlayerData['Pos'] == 'WR') & (allPlayerData["Snap"] > 15)]
# Create a new wrData to store sorted player stats
# This line is for testing / displaying week and player
sortedPlayerDf2 = pd.DataFrame(columns=['Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                       'Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                       'Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                       'Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])
# sortedPlayerDf = sortedPlayerDf.loc[:, ~sortedPlayerDf2.columns.isin(['Player', 'Week'])]
# print(sortedPlayerDf2.head())
sortedPlayerDf = pd.DataFrame(columns=['Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                       'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                       'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])
# Linear regression model
model = LinearRegression()

for player in wrData['Player']:
    # Set curPlayer to a wrData that contains the all appearances of the current players stats
    curPlayer = wrData.loc[wrData['Player'] == player]
    #print(curPlayer)

    # Check that the player has played at least 3 games, if not continue to the next player
    if not len(curPlayer) >= 3:
        continue

    # Go from i to the end of the window size, in this case its 3
    for i in range(len(curPlayer) - 3 + 1):
        # Create a new wrData to store the last 3 weeks
        curWeekStats = []
        curWeekStats2 = []
        # Creates a list of indices where the current player appears in wrData
        indices = list(curPlayer.index.values)

        # Get a "window" of three games into curWeekStats
        for j in range(3):
            # FullStatLine is the current players' stat line at Index i + j.
            # Ex: J is the window size, and i is the starting point.
            fullStatLine = curPlayer.loc[indices[i+j]]
            # FixedStatLine is only a few stats taken from the full statline which are put into a list
            fixedStatLine2 = fullStatLine[['Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD']].values.tolist()
            fixedStatLine = fullStatLine[['Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD']].values.tolist()
            # CurWeekStats is a list that will contain an array of the players stats from week i to the window size
            curWeekStats.append(fixedStatLine)
            curWeekStats2.append(fixedStatLine2)

        print(player, "          Stats: ", curWeekStats2)
        # Convert curWeekStats from a list to a numpy array
        npArr = np.asarray(curWeekStats)
        npArr2 = np.asarray(curWeekStats2)

        # linear regression
        reg = model.fit(npArr[:2], npArr[:2])
        pred = reg.predict([npArr[2]])

        # turn the 2d array that is pred [[pred]] to a 1d array [pred]
        predList = np.ravel(np.around(pred, 2))
        # Add the player name a 0 for week to the front of the predList values so its "readable"
        arrg = [player, 0] + predList.tolist()

        # Flatten the numpy array
        npArr = npArr.flatten()
        # Flatten the np array and append the predList to it
        npArr2 = npArr2.flatten()
        npArr2 = np.concatenate((npArr2, arrg), axis=0)
        print(npArr2.tolist())

        # Append the flattened numpy array to the sortedPlayerdf
        sortedPlayerDf.loc[len(sortedPlayerDf)] = npArr
        # Append it to the df containing names
        sortedPlayerDf2.loc[len(sortedPlayerDf2)] = npArr2

np.set_printoptions(linewidth=100)
pd.set_option('display.max_columns', None)
print(sortedPlayerDf.head(100))


def getList():
    return sortedPlayerDf2
