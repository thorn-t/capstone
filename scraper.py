import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests


def getTeams(theSoup):
    teamList = set()
    # Find the <div> element with id "div_player_offense" and get the <tbody> tag inside it
    player_offense_div = theSoup.find("div", {"id": "div_player_offense"})
    tbody = player_offense_div.find("tbody")

    # Find all <tr> tags in the <tbody> tag and get the team names from the "tm" column
    for tr in tbody.find_all("tr"):
        td = tr.find("td", {"data-stat": "team"})
        if td is not None:
            teamList.add(td.text.strip())
    teamList = list(teamList)

    return teamList

chrome_driver_path = "D:\ChromeDriver\chromedriver.exe"

options = webdriver.ChromeOptions
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)


with open("new.csv", "w", newline="") as f:
    # Create the csv and make the header
    table_to_csv = csv.writer(f)
    header = ["Player", "PID", "Pos", "Week", "Tm", "Opp", "Cmp", "PassAtt", "PassYds", "PassTD", "Int", "Sacked", "YardsLostSack", "PassLng", "Rate", "RushAtt",
              "RushYards", "RushTD", "RushLng", "Tgt", "Rec", "RecYds", "RecTD", "RecLng", "Fmb", "FL", "Snap", "Snap%"]
    table_to_csv.writerow(header)
    ##################################### SINGLE GAME SCRAPE STARTS HERE ######################################
    # Navigate to the current game page
    # driver.get("file:///D:/PycharmProjects/NFLScraper/Wild%20Card%20-%20Seattle%20Seahawks%20at%20San%20Francisco%2049ers"
    #            "%20-%20January%2014th,%202023%20_%20Pro-Football-Reference.com.html")
    driver.get("https://www.pro-football-reference.com/boxscores/202211270kan.htm")
    # Get the entire page html
    theHtml = driver.page_source
    # Find the table using beautiful soup
    soup = BeautifulSoup(theHtml, "html.parser")
    offenseTable = soup.findAll(id="div_player_offense")[0]
    allRows = offenseTable.findAll("tr")


    # Make a list of [player name, player ID]
    playerID = []
    for row in allRows:
        # Get the player IDs from the table
        for cell in row.findAll(["td", "th"]):
            # Sometimes it grabs None types and puts them in the array, this just makes sure it doesn't do that.
            if cell.get("data-append-csv") is not None:
                playerID.append(cell.get_text())
                playerID.append(cell.get("data-append-csv"))


    # Make a list containing [Player, Pos, Num, Pct, Num, Pct, Num, Pct]
    homeSnapsTable = soup.findAll(id="home_snap_counts")[0]
    awaySnapsTable = soup.findAll(id="vis_snap_counts")[0]
    homeSnapsRows = homeSnapsTable.findAll("tr")
    awaySnapsRows = awaySnapsTable.findAll("tr")
    offensiveSnapCounts = []
    for row in homeSnapsRows:
        rowData = []
        # Get the single players name / position / snap counts / snap % and more into a list called rowData
        for cell in row.findAll(["td", "th"]):
            rowData.append(cell.get_text())
        # rowData[1] is the position of the player in the table. This makes sure to print only offensive players
        if rowData[1] in ["QB", "RB", "WR", "TE", "FB"]:
            offensiveSnapCounts.append(rowData)

    for row in awaySnapsRows:
        rowData = []
        # Get the single players name / position / snap counts / snap % and more into a list called rowData
        for cell in row.findAll(["td", "th"]):
            rowData.append(cell.get_text())
        # rowData[1] is the position of the player in the table. This makes sure to print only offensive players
        if rowData[1] in ["QB", "RB", "WR", "TE", "FB"]:
            offensiveSnapCounts.append(rowData)

    #print(offensiveSnapCounts)

    # for row in offensiveSnapCounts:
    #     print("Name: ", row[0], "Pos: ", row[1])

    # Get the two teams into the teams list
    teams = []
    teams = getTeams(soup)

    # Create the CSV appending player IDs, snap counts, opposing team, and player stats
    for row in allRows:
        row_data = []

        for cell in row.findAll(["td", "th"]):
            row_data.append(cell.get_text())
            #print("ROW DATA: ", row_data)
            # Try to put the playerIDs in
            try:
                # Check if the rowData[0] player name matches the playerID name
                if row_data[0] == playerID[0]:
                    row_data.insert(1, playerID[1])
                    row_data.insert(4, 3)
                    playerID.pop(0)
                    playerID.pop(0)
            except IndexError as e:
                print("The index is out of range Idk if this is fine but w/e it works for now: ", e)

        # This tries to be the header in the file, but I don't want it, so I make it go to the next iteration
        if "Passing" in row_data or "Player" in row_data:
            continue

        for q in range(len(offensiveSnapCounts)):
            #print("ROW: ", row_data[0], " SNAP: ", offensiveSnapCounts[q][0])
            if row_data[0] == offensiveSnapCounts[q][0]:
                #print("BANNNNG")
                row_data.insert(2, offensiveSnapCounts[q][1])
                # Append the number of snaps to the end of the players row
                row_data.append(offensiveSnapCounts[q][2])
                # Append the snap % to the end of the players row
                row_data.append(offensiveSnapCounts[q][3])

        # Insert the opposing team name into the array row_data[4] contains the players team, teams contains both teams
        # this inserts the opposing team into the array.
        if row_data[4] == teams[0]:
            row_data.insert(5, teams[1])
        else:
            row_data.insert(5, teams[0])

        # Checks to see if the 4th item in the array is not an int. This is to keep punters out of the data set
        # because during the scraping they were sneaking in from the offense table and missing rows.
        if type(row_data[3]) != int:
            continue

        print(row_data)
        table_to_csv.writerow(row_data)
#####################################  SINGLE GAME SCRAPE ENDS HERE  ######################################



driver.quit()