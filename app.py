from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from markupsafe import Markup
import sortcsv
from fpcalc import getNamesAndFp
import numpy as np
from tabulate import tabulate
from main import *

app = Flask(__name__)


# All html files must be in the templates folder
allPlayerData = pd.read_csv('Weeks 1-7 (2).csv')
teams = np.sort(allPlayerData["Tm"].unique())

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/players/all")
def getAllPlayers():
    # df is the flattened df from sortcsv
    df = pd.read_csv('NFLPred.csv')
    print(df.columns)
    df = df.drop(["Player.1", "Player.2"], axis=1)
    # create a dictionary
    # key = old name
    # value = new name
    dict = {'Week': 'Week 0',
            'Tgt': 'Targets 0',
            'Rec': 'Rec 0',
            'RecYds': 'RecYds 0',
            'Snap': 'Snap 0',
            'RecTD': 'RecTD 0',
            'Week.1': 'Week 1',
            'Tgt.1': 'Tgt 1',
            'Rec.1': 'Rec 1',
            'RecYds.1': 'RecYds 1',
            'Snap.1': 'Snap 1',
            'RecTD.1': 'RecTD 1',
            'Week.2': 'Week 2',
            'Tgt.2': 'Tgt 2',
            'Rec.2': 'Rec 2',
            'RecYds.2': 'RecYds 2',
            'Snap.2': 'Snap 2',
            'RecTD.2': 'RecTD 2',
            }

    # call rename () method
    df.rename(columns=dict,
              inplace=True)

    # dfHtml is df in a safe html form so jinja will render it
    dfHtml = Markup(df.to_html())
    return render_template("allplayers.html", dfHtml=dfHtml)
    #return "OKAY"


@app.route("/admin")
def getAdminPage():
    return render_template("admin.html")


@app.route('/admin', methods=['POST'])
def my_form_post():
    text = request.form.get('text')
    if text == "Train with recent data":
        trainWithRecentData()
        text = "Finished, check all players page"
    if text == "Check for new data":
        text = checkForNewData()
    return render_template("admin.html", ptext=text)


@app.route('/team', methods=['GET', 'POST'])
def getTeamPage():
    # If the user selects and submits a team display the getTeamDvpPage
    if request.method == 'POST':
        # Get the team selected from the combobox on the page
        selectedTeam = request.form.get('teamSelect')
        # Redirect the url and pass the team name
        return redirect(url_for('getTeamDvpPage', teamName=selectedTeam))
    else:
        return render_template("team.html", teams=teams)


@app.route('/teamdvp/<teamName>')
def getTeamDvpPage(teamName):
    # Set the teams data
    teamData = allPlayerData.loc[(allPlayerData['Opp'] == teamName)]
    teamData = getNamesAndFp(teamData)
    print(teamData["Week"].max())
    allWeeks = []
    # Go from week 1 to the maximum week in the datasheet
    for week in range(1, teamData["Week"].max()+1):
        curWeek = []
        # Get player data at each position, on the current week, sorted by fp values. .loc[:value] is how many players
        # show up in the list. so if .iloc[:2] then a max of 2 players will show up.
        qbData = teamData.loc[(teamData['Pos'] == 'QB') & (teamData["Week"] == week)].sort_values('Fpts', ascending=False).iloc[:2].values.tolist()
        rbData = teamData.loc[(teamData['Pos'] == 'RB') & (teamData["Week"] == week)].sort_values('Fpts', ascending=False).iloc[:2].values.tolist()
        wrData = teamData.loc[(teamData['Pos'] == 'WR') & (teamData["Week"] == week)].sort_values('Fpts', ascending=False).iloc[:3].values.tolist()
        teData = teamData.loc[(teamData['Pos'] == 'TE') & (teamData["Week"] == week)].sort_values('Fpts', ascending=False).iloc[:2].values.tolist()

        # Append all data to an array and fill it in to make sure it is always equal length.
        curWeek.append(qbData)
        print("Cur week: ", curWeek)
        if len(curWeek[0]) < 2:
            curWeek[0].append(["None", "QB", "None", "None", 0.0])
        print("Cur week: ", curWeek)
        curWeek.append(rbData)
        if len(curWeek[1]) < 2:
            curWeek[1].append(["None", "RB", "None", "None", 0.0])
        curWeek.append(wrData)
        if len(curWeek[2]) < 3:
            curWeek[2].append(["None", "WR", "None", "None", 0.0])
        curWeek.append(teData)
        if len(curWeek[3]) < 2:
            curWeek[3].append(["None", "TE", "None", "None", 0.0])

        # Append everything to this array containing data for every week
        allWeeks.append(curWeek)

    # Create a new array to hold player data in the format [pos, player, fpts] to display to user
    playerData = []
    for i in range(len(allWeeks)):
        cur = []
        print(allWeeks[i])
        for j in range(len(allWeeks[i])):
            for p in range(len(allWeeks[i][j])):
                cur.append(allWeeks[i][j][p][1])
                cur.append(allWeeks[i][j][p][0])
                cur.append(allWeeks[i][j][p][4])
        playerData.append(cur)

    #print(playerData)
    #allWeeks = np.array(allWeeks)
    # Convert the data to html
    #teamData = Markup(teamData.to_html())
    #return render_template("teamdvp.html", teamName=teamName, teamData=teamData)
    return render_template("teamdvp.html", teamName=teamName, teamData=Markup(tabulate(playerData, tablefmt='html')))


def trainWithRecentData():
    df = sortcsv.main()
    print("The trainWithRecentData test function runs")



def checkForNewData():
    print("The checkForNewData test function runs")
    textToReturn = main()
    if textToReturn == "up to date":
        return "up to date"
    else:
        scrapeFromCurrentWeek(textToReturn[0], textToReturn[1])
        return f"Scraped from week {textToReturn[0]} to week {len(textToReturn[1]) - 1}."


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
    #app.run(debug=True)
