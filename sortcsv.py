import numpy as np
import pandas as pd

df = pd.read_csv('Weeks 1-7.csv')

# Create a new df to store sorted player stats
sortedPlayerDf = pd.DataFrame(columns=['Player', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                       'Player', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD',
                                       'Player', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD'])
for player in df['Player']:
    # Set curPlayer to a df that contains the all appearances of the current players stats
    curPlayer = df.loc[df['Player'] == player]
    #print(curPlayer)

    # Check that the player has played at least 3 games, if not continue to the next player
    if not len(curPlayer) >= 3:
        continue

    # test = sortedPlayerDf.to_numpy()
    # print("TEST ", curPlayer.to_numpy().flatten())

    # Go from i to the end of the window size, in this case its 3
    for i in range(len(curPlayer) - 3 + 1):
        # Create a new df to store the last 3 weeks
        curWeekStats = []
        # Creates a list of indices where the current player appears in df
        indices = list(curPlayer.index.values)

        for j in range(3):
            # FullStatLine is the current players stat line at Index i + j.
            # Ex: J is the window size, and i is the starting point.
            fullStatLine = curPlayer.loc[indices[i+j]]
            # FixedStatLine is only a few stats taken from the full statline which are put into a list
            fixedStatLine = fullStatLine[['Player', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD']].values.tolist()
            # CurWeekStats is a list that will contain an array of the players stats from week i to the window size
            curWeekStats.append(fixedStatLine)

        print(player, "          Stats: ", curWeekStats)
        # Convert curWeekStats from a list to a numpy array
        npArr = np.asarray(curWeekStats)
        print(npArr)
        # Flatten the numpy array
        npArr = npArr.flatten()
        # Append the flattened numpy array to the sortedPlayerDf
        sortedPlayerDf.loc[len(sortedPlayerDf)] = npArr

np.set_printoptions(linewidth=100)
pd.set_option('display.max_columns', None)
print(sortedPlayerDf.head(100))


def getList():
    return sortedPlayerDf
