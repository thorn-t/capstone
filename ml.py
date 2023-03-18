from sklearn import metrics
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# sns.set_style('whitegrid')
#
# #
# # examp_df = pd.DataFrame({
# #  'ff_points_lag_1': [12, 20, 45, 68, 98], # lag means previous, 1 means this was last year, 2 would've meant 2 year ago, etc.
# #  'snapcount_lag_1': [10, 13, 14, 65, 70],
# #  'ff_points_next_year': [15, 40, 50, 55, 80]
# # })
# #
# # examp_df.plot(x='ff_points_lag_1', y='ff_points_next_year', kind='scatter')
# #
# # plt.show()
# # sns.regplot(x=examp_df['ff_points_lag_1'], y=examp_df['ff_points_next_year'])
# # plt.show()
# # print(examp_df.head())
#
#
# pd.set_option('display.max_columns', None)
#
# df = pd.read_csv("tester.csv")
#
# print(df.head())
#
# print(df['Week'].min(), df['Week'].max())
#
# df = df.groupby(['PID', 'Tm', 'Player', 'Pos', 'Week'], as_index=False) \
#     .agg({
#     'Snap': np.sum,
#     # 'Snap%': np.mean,
#     'Rate': np.mean,
#     'PassYds': np.sum,
#     'PassTD': np.sum,
#     'Att': np.sum,
#     'RecYds': np.sum,
#     'RecTD': np.sum,
#     'Rec': np.sum,
#     'Tgt': np.sum,
#     'PassLng': np.sum,
#     'Att.1': np.sum,
#     'RushYards': np.sum,
#     'RushTD': np.sum,
#     'RushLng': np.sum,
#     'PprFP': np.sum,
# })
#
# print(df.head())
# # df.plot(x='Week', y='Snap', kind='scatter')
# # plt.show()
#
# pd.set_option('chained_assignment', None)
#
# lag_features = ['Att.1',
#                 'Tgt',
#                 'RecYds',
#                 'Snap',
#                 'Rate',
#                 'Att',
#                 'PassTD',
#                 'PprFP', ]
#
# for lag in range(1, 8):
#
#     """
#     We have not talked about shift before.
#     Shift moves our data down by the number of rows we specify.
#
#     pandas.DataFrame.shift documentation
#
#     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shift.html
#     """
#
#     shifted = df.groupby('PID').shift(lag)
#
#     for column in lag_features:
#         """
#         Python f-strings are similar to using the format string method, although a bit cleaner
#
#         Article on Python f-strings
#
#         https://realpython.com/python-f-strings/
#         """
#         df[f'lag_{column}_{lag}'] = shifted[column]
#
# df = df.fillna(-1)
# print(df.head())
#
# """
# Correlation matrix for all positions
# """
# print(df.corr()[['PprFP']])
# """
# Correlation matrix for just wide receivers.
# """
# pd.set_option('display.max_rows', 65)
# print(df.loc[df['Pos'] == 'WR'].corr()[['PprFP']])
#
# wr_df = df.loc[(df['Pos'] == 'WR')]
# print(wr_df.shape)
# wr_df = wr_df.loc[wr_df['lag_Snap_1'] > 25]
# print(wr_df.shape)
# sns.residplot(x=wr_df['lag_Snap_1'], y=wr_df['PprFP'])
# # plt.show()
#
# """
# This is our feature matrix.
# """
# print("FEATURE TIME")
# X = wr_df[['lag_Tgt_1', 'lag_RecYds_1', 'lag_Snap_1', 'lag_PprFP_1']].values
# y = wr_df['PprFP'].values
# print(X.shape, y.shape)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
# lr = LinearRegression()
# lr.fit(X_train, y_train)
# y_pred = lr.predict(X_test)
# print(mean_absolute_error(y_pred, y_test))
#
#
# pd.set_option('display.max_rows', None)
#
# wr_df_pred = df.loc[
#     (df['Pos'] == 'WR') & (df['Snap'] > 25),
#     ['Player', 'Tgt', 'RecYds', 'Snap', 'PprFP']
# ]
#
# wr_df_pred['PredFP'] = lr.predict(wr_df_pred[['Tgt', 'Snap', 'RecYds', 'PprFP']].values)
#
# wr_df_pred = wr_df_pred.rename(columns = {'PprFP':'actualFP'})
# print("ERM?")
# print(wr_df_pred.sort_values(by='PredFP', ascending=False).head(100))


# Load in data
playerData = pd.read_csv("tester.csv")
print(playerData.head())

# Display starting and ending week to make sure I load the right csv
print(f"Starting week: {playerData['Week'].min()} | Ending week: {playerData['Week'].max()}")

# Prepare the table for WRs
# Grab only the WRs from player data who played at least 15 snaps
linWRData = playerData.loc[(playerData['Pos'] == 'WR') & (playerData["Snap"] > 15)]
print(linWRData.head())
# Create new table containing only WR relevant information
linWRData = linWRData[[
    'Player',
    'PID',
    'Week',
    'Tgt',
    'Rec',
    'RecYds',
    'Snap',
    'RecTD',
    'FL',
    'PprFP',
]].copy()
print(linWRData.head())

# go from week 7 to 1
# weeksSince = 0
# for week in range(7, 0, -1):
#     print(week)
#     for item in linWRData.loc[(linWRData['Week']) == str(week)]:
#         print(item)
print("YO")
# Make dfs where weeks are 5-7, 3-7, and 1-7
last3 = linWRData.loc[linWRData['Week'].isin([5, 6, 7])]
last5 = linWRData.loc[linWRData['Week'].isin([3, 4, 5, 6, 7])]
last7 = linWRData.loc[linWRData['Week'].isin([1, 2, 3, 4, 5, 6, 7])]
# print(last7.sort_values(by='Week', ascending=True).head(100))

# Create a new df to avg it all together (this one does last 3 for now)
avgDf = pd.DataFrame(columns=['Player', 'PID', 'Week', 'Tgt', 'Rec', 'RecYds', 'Snap', 'RecTD', 'FL',
                              'PprFP', '3RecYds', '3Tgt', '3Rec', '3Snap'])
# Put together my new df with the added headers and plug in all week 7 data to it
avgDf = pd.concat([avgDf, last3.loc[last3['Week'] == 7]])

# For each player in last3 weeks do this
for player in last3['Player']:
    # print(avgDf.loc[avgDf['Player'] == player])
    # Set curPlayer to a df that contains the current players stats for up to the last 3 games
    curPlayer = last3.loc[last3['Player'] == player]
    # Sum together the current players last 3 "relevant stats" stats
    avgDf.loc[avgDf.Player == player, '3RecYds'] = curPlayer['RecYds'].sum()
    avgDf.loc[avgDf.Player == player, '3Tgt'] = curPlayer['Tgt'].sum()
    avgDf.loc[avgDf.Player == player, '3Rec'] = curPlayer['Rec'].sum()
    avgDf.loc[avgDf.Player == player, '3Snap'] = curPlayer['Snap'].sum()
    # print(last3.loc[last3['Player'] == player])
    # print(curPlayer['RecYds'].sum())
    # print("~~~~~~~~~~~~~~~~~")
# print(avgs.head())
# print(avgs.columns)
print(avgDf.head())
# Get a sample of 20% of the data
linHoldout = avgDf.sample(frac=0.20)
# Remove the 20% of data and set linTraining to the remaining 80%
linTraining = avgDf.loc[~avgDf.index.isin(linHoldout.index)]
# Display Size
print(f"Train size: {len(linTraining)} | Total size: {len(avgDf)}")
print(linTraining.head())

# Make df that contains just features for training
featuresTrain = linTraining[["3RecYds", "3Tgt", "3Rec", "3Snap"]].values
# Make df that contains only the targets for training
targetTrain = linTraining["RecYds"].values

# featuresTrain = linTraining[["last3Tgt", "last5Tgt", "lastXTgt", "last3Rec", "last5Rec", "lastXRec", "last3RecYds",
#                              "last5RecYds", "lastXRecYds", "last3RecTD", "last5RecTD", "lastXRecTD", "last3Snap",
#                              "last5Snap", "lastXSnap", "last3FL", "last5FL", "lastXFL"]].values
# targetTrain = linTraining[["Tgt", "Rec", "RecYds", "RecTD", "Snap", "FL"]].values

# Make df that contains just features for testing
featuresTest = linHoldout[["3RecYds", "3Tgt", "3Rec", "3Snap"]].values
# Make df that contains only the targets for testing
targetTest = linHoldout["RecYds"].values

# regression
model = LinearRegression()
reg = model.fit(featuresTrain, targetTrain)
print(f"R squared (train): {model.score(featuresTrain, targetTrain)}")

# create df of predictions based on test features
pred = reg.predict(featuresTest)
# Compare predictions to actual values
variance = metrics.r2_score(targetTest, pred)
print(f"Variance score (test): {variance}")
print(f"Mean absolute error: {mean_absolute_error(pred, targetTest)}")
avgDf['PredRecYds'] = model.predict(avgDf[["3RecYds", "3Tgt", "3Rec", "3Snap"]].values)
avgDf = avgDf.rename(columns={'RecYds': 'actualRecYds'})
print("YOOO?")
np.set_printoptions(linewidth=100)
pd.set_option('display.max_columns', None)
print(avgDf.sort_values(by='PredRecYds', ascending=False).head(100))










# linHoldout = linWRData.sample(frac=0.20)
# linTraining = linWRData.loc[~linWRData.index.isin(linHoldout.index)]
# print(f"Train size: {len(linTraining)} | Total size: {len(linWRData)}")
#
# print(linTraining.head())
# featuresTrain = linTraining[["Tgt", "Rec", "RecYds", "RecTD", "Snap", "FL"]].values
# targetTrain = linTraining["PprFP"].values
#
# # featuresTrain = linTraining[["last3Tgt", "last5Tgt", "lastXTgt", "last3Rec", "last5Rec", "lastXRec", "last3RecYds",
# #                              "last5RecYds", "lastXRecYds", "last3RecTD", "last5RecTD", "lastXRecTD", "last3Snap",
# #                              "last5Snap", "lastXSnap", "last3FL", "last5FL", "lastXFL"]].values
# # targetTrain = linTraining[["Tgt", "Rec", "RecYds", "RecTD", "Snap", "FL"]].values
#
# featuresTest = linHoldout[["Tgt", "Rec", "RecYds", "RecTD", "Snap", "FL"]].values
# targetTest = linHoldout["PprFP"].values
#
# model = LinearRegression()
# reg = model.fit(featuresTrain, targetTrain)
# print(f"R squared (train): {model.score(featuresTrain, targetTrain)}")
#
# pred = reg.predict(featuresTest)
# variance = metrics.r2_score(targetTest, pred)
# print(f"Variance score (test): {variance}")
#
# week8Data = pd.read_csv("Week 8.csv")
# week8Data = week8Data.loc[(week8Data['Pos'] == 'WR')]
# week8Data = week8Data[[
#                 'Player',
#                 'PID',
#                 'Week',
#                 'Tgt',
#                 'Rec',
#                 'RecYds',
#                 'Snap',
#                 'RecTD',
#                 'FL',
#                 'PprFP',
#                 ]].copy()
#
# week8Data['PredFP'] = model.predict(week8Data[["Tgt", "Rec", "RecYds", "RecTD", "Snap", "FL"]].values)
#
# week8Data = week8Data.rename(columns = {'PprFP':'actualFP'})
# print("ERM?")
# print(week8Data.sort_values(by='PredFP', ascending=False).head(100))
#
