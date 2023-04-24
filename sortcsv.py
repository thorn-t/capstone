from sklearn import metrics
from sklearn.linear_model import LinearRegression, PoissonRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import pandas as pd


def calculateAverages(df, real):

    #df2 = df[['Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD']].mean()
    tgtAvg = (df[:, 0] + df[:, 5]) / 2
    #print("Avg: ", tgtAvg, " Real: ", real[:, 0])
    #print("TGT AVG SHAPE: ", tgtAvg.shape, " REAL SHAPE: ", real[:, 0].shape)
    print("Mean absolute error tgt AVGS: ", mean_absolute_error(tgtAvg, real[:, 0]))

    recAvg = (df[:, 1] + df[:, 6]) / 2
    #print("Avg: ", recAvg, " Real: ", real[:, 1])
    #print("REC AVG SHAPE: ", recAvg.shape, " REAL SHAPE: ", real[:, 1].shape)
    print("Mean absolute error rec AVGS: ", mean_absolute_error(tgtAvg, real[:, 1]))

    recYdsAvg = (df[:, 2] + df[:, 7]) / 2
    #print("Avg: ", recYdsAvg, " Real: ", real[:, 2])
    #print("RECYDS AVG SHAPE: ", recYdsAvg.shape, " REAL SHAPE: ", real[:, 2].shape)
    print("Mean absolute error recyds AVGS: ", mean_absolute_error(tgtAvg, real[:, 2]))

    snapAvg = (df[:, 3] + df[:, 8]) / 2
    # print("Avg: ", snapAvg, " Real: ", real[:, 3])
    # print("Snap% AVG SHAPE: ", snapAvg.shape, " REAL SHAPE: ", real[:, 3].shape)
    print("Mean absolute error snap AVGS: ", mean_absolute_error(snapAvg, real[:, 3]))

    tdAvg = (df[:, 4] + df[:, 9]) / 2
    #print("Avg: ", tdAvg, " Real: ", real[:, 4])
    # print("td AVG SHAPE: ", tdAvg.shape, " REAL SHAPE: ", real[:, 4].shape)
    print("Mean absolute error td AVGS: ", mean_absolute_error(tdAvg, real[:, 4]))
    # dataInput = sortedPlayerDf[:,0:10]
    # dataOutput = sortedPlayerDf[:,10:]
    # print("Data shapes:", dataInput.shape, dataOutput.shape)
    # # linear regression
    # reg = model.fit(dataInput, dataOutput)
    # pred = reg.predict(dataInput)
    #
    # comparePred = np.concatenate((dataOutput, pred), axis=1)
    # print("Comparepred: ", comparePred.shape)


def main():
    allPlayerData = pd.read_csv('Weeks 1-7 (2).csv')
    wrData = allPlayerData.loc[(allPlayerData['Pos'] == 'WR') & (allPlayerData["Snap"] > 15)]
    # Create a new wrData to store sorted player stats
    # This line is for testing / displaying week and player
    sortedPlayerDf2 = pd.DataFrame(columns=['Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                            'Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                            'Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])
    # sortedPlayerDf = sortedPlayerDf.loc[:, ~sortedPlayerDf2.columns.isin(['Player', 'Week'])]
    # print(sortedPlayerDf2.head())
    sortedPlayerDf = pd.DataFrame(columns=['Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                           'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                           'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])

    finalWeekDf = pd.DataFrame(columns=['Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                        'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                        'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])
    # Linear regression model
    model = LinearRegression()

    for player in wrData['Player']:
        # Set curPlayer to a wrData that contains the all appearances of the current players stats
        curPlayer = wrData.loc[wrData['Player'] == player]
        # print(curPlayer)

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
                fullStatLine = curPlayer.loc[indices[i + j]]
                # FixedStatLine is only a few stats taken from the full statline which are put into a list
                fixedStatLine = fullStatLine[['Tgt', 'Rec', 'RecYds', 'Snap%', 'RecTD']].values.tolist()
                fixedStatLine2 = fullStatLine[['Player', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap%', 'RecTD']].values.tolist()
                curWeekStats.append(fixedStatLine)
                curWeekStats2.append(fixedStatLine2)

            #print(player, "          Stats: ", curWeekStats2)
            # Convert curWeekStats from a list to a numpy array
            npArr = np.asarray(curWeekStats)
            npArr2 = np.asarray(curWeekStats2)

            # Flatten the numpy array
            npArr = npArr.flatten()
            # Flatten the np array and append the predList to it
            npArr2 = npArr2.flatten()
            #npArr2 = np.concatenate((npArr2, arrg), axis=0)
            #print(npArr2.tolist())

            # See if it is the most recent week, if not append to curWeekStats
            if i != (len(curPlayer) - 3):
                # Append the flattened numpy array to the sortedPlayerdf
                sortedPlayerDf.loc[len(sortedPlayerDf)] = npArr
                # Append it to the df containing names
                sortedPlayerDf2.loc[len(sortedPlayerDf2)] = npArr2
            else:
                # Append to finalWeekDf
                finalWeekDf.loc[len(sortedPlayerDf)] = npArr


    sortedPlayerDf = sortedPlayerDf.to_numpy()
    #print("sortedplayerdf2: ", sortedPlayerDf2.shape)
    dataInput = sortedPlayerDf[:,0:10]
    dataOutput = sortedPlayerDf[:,10:]
    print("Training avgs")
    calculateAverages(dataInput, dataOutput)
    #print("Data shapes:", dataInput.shape, dataOutput.shape)
    # linear regression
    reg = model.fit(dataInput, dataOutput)
    pred = reg.predict(dataInput)

    comparePred = np.concatenate((dataOutput, pred), axis=1)
    #print("Comparepred: ", comparePred.shape)
    print("Training DF")
    x, y = pred[:, 0], dataOutput[:, 0]
    print("Mean absolute error tgt: ", mean_absolute_error(x, y))

    x, y = pred[:, 1], dataOutput[:, 1]
    print("Mean absolute error rec: ", mean_absolute_error(x, y))

    x, y = pred[:, 2], dataOutput[:, 2]
    print("Mean absolute error recyds: ", mean_absolute_error(x, y))

    x, y = pred[:, 3], dataOutput[:, 3]
    print("Mean absolute error snap: ", mean_absolute_error(x, y))

    x, y = pred[:, 4], dataOutput[:, 4]
    print("Mean absolute error td: ", mean_absolute_error(x, y))

    # turn the 2d array that is pred [[pred]] to a 1d array [pred]
    #predList = np.ravel(np.around(pred, 2))
    # Add the player name a 0 for week to the front of the predList values so its "readable"
    #arrg = [player, 0] + predList.tolist()

    #np.set_printoptions(linewidth=100)
    np.set_printoptions(threshold=np.inf, suppress=True)
    pd.set_option('display.max_columns', None)
    #print(comparePred)

    # calc mean absolute error manually and get the highest and lowest values
    # average all the samples for each set in training and testing then get mean error to precit that and see how it compares
    finalWeekDf = finalWeekDf.to_numpy()
    finalInput = finalWeekDf[:, 0:10]
    finalOutput = finalWeekDf[:, 10:]
    #print("Data shapes:", finalInput.shape)
    finalPred = reg.predict(finalInput)
    print("Testing avgs")
    calculateAverages(finalInput, finalOutput)
    #print(sortedPlayerDf)
    #print(pred)
    print("Testing DF")
    compareFinal = np.concatenate((finalOutput, finalPred), axis=1)

    np.savetxt("finalOutput.csv", finalOutput, delimiter=",", fmt='%f')
    np.savetxt("finalPred.csv", finalPred, delimiter=",", fmt='%f')

    x, y = finalPred[:, 0], finalOutput[:, 0]
    print("Mean absolute error tgt: ",mean_absolute_error(x, y))

    x, y = finalPred[:, 1], finalOutput[:, 1]
    print("Mean absolute error rec: ", mean_absolute_error(x, y))

    x, y = finalPred[:, 2], finalOutput[:, 2]
    print("Mean absolute error recyds: ", mean_absolute_error(x, y))

    x, y = finalPred[:, 3], finalOutput[:, 3]
    print("Mean absolute error snap: ", mean_absolute_error(x, y))

    x, y = finalPred[:, 4], finalOutput[:, 4]
    print("Mean absolute error td: ", mean_absolute_error(x, y))

    #print(compareFinal)
    return sortedPlayerDf2




if __name__ == "__main__":
    main()

