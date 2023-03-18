import numpy as np
import pandas as pd

df = pd.read_csv('Weeks 1-7.csv')



for player in df['Player']:
    # Set curPlayer to a df that contains the current players stats for up to the last 3 games
    curPlayer = df.loc[df['Player'] == player]
    print(curPlayer)
    print(len(curPlayer))
    # Check that the player has played at least 3 games, if not continue to the next player
    if not len(curPlayer) >= 3:
        continue
    sortedDf = pd.DataFrame(columns=['Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])
    vales = [2,3,4,5,6]
    sortedDf.loc[len(sortedDf)] = vales
    # test = sortedDf.to_numpy()
    # print("TEST ", curPlayer.to_numpy().flatten())

    print(sortedDf)
    sortedDf.loc[len(sortedDf)] = vales
    newDf = curPlayer.loc[curPlayer['Tgt']]
    # sortedDf = sortedDf.assign(Tgt=[1],
    #                 Rec=[2],
    #                 RecYds=[3],
    #                 Snap=[4],
    #                 RecTD=[5])
    print("SORT:",sortedDf)
    vales = [2,3,3,2,1]
    sortedDf.loc[len(sortedDf)] = vales
    # sortedDf = sortedDf.assign(Tgt=[5],
    #                            Rec=[6],
    #                            RecYds=[7],
    #                            Snap=[8],
    #                            RecTD=[9])
    print(sortedDf.loc[0+2].tolist())
    print("__________________________________ CHECK")


    for i in range(len(curPlayer) - 3 + 1):
        # Create a new df to store the last 3 weeks
        sortedDf = pd.DataFrame(columns=['Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])
        curWeekStats = []
        indices = list(curPlayer.index.values)
        print("INDICIES", indices)
        print("I IS: ", i)
        for j in range(3):
            print("J IS: ", j)
            curWeekStats.append(curPlayer.loc[indices[i+j]].tolist())
            print(curWeekStats)

        sortedDf.loc[len(sortedDf)] = curWeekStats



print(type(df))
df = df.to_numpy()
print("___")
print(type(df))