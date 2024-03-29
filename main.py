import random
import time
import pandas as pd
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
import os

#chrome_driver_path = "D:\ChromeDriver\chromedriver.exe"
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#service = Service(executable_path=chrome_driver_path)
#driver = webdriver.Chrome(service=service, options=options)


# driver = webdriver.Chrome(ChromeDriverManager().install())

"""
    The purpose of getWeekLinks is to get passed a link to a year page and create an array containing links to all
    weeks played that year.
"""
def getWeekLinks():
    # Navigate to score page
    # driver.get("file:///D:/PycharmProjects/NFLScraper/2022%20NFL%20Week%2019%20Leaders%20&%20Scores%20_%20Pro-Football-Reference.com.html")
    cwd = os.getcwd()
    driver.get(f"{cwd}/2022%20NFL%20Week%2018%20Leaders%20&%20Scores%20_%20Pro-Football-Reference.com.html")
    #driver.get(
    #    "file:///D:/PycharmProjects/NFLScraper/2022%20NFL%20Week%2018%20Leaders%20&%20Scores%20_%20Pro-Football-Reference.com.html")
    #driver.get("https://www.pro-football-reference.com/years/2022/week_22.htm")
    # driver.get("file:///D:/PycharmProjects/NFLScraper/Wild%20Card%20-%20Seattle%20Seahawks%20at%20San%20Francisco%2049ers"
    #            "%20-%20January%2014th,%202023%20_%20Pro-Football-Reference.com.html")


    # Adjust the headers
    # write sentence in report in future work about live website not working
    # have the data committed (html file)
    # SVR in scikit learn

    # Get all week links into a list weekLinks. List starts at index 1 to match week 1 link
    a = driver.page_source
    soup = BeautifulSoup(a, "html.parser")
    # Get all html within this id into weekLinks
    weekLinks = soup.findAll(id="div_week_games")[0]
    # Get all anchor tags into weekLinks
    weekLinks = weekLinks.findAll("a")
    # Change from anchor tags to actual links in weekLinks
    for i in range(len(weekLinks)):
        weekLinks[i] = weekLinks[i].get("href")
    # Insert a "" at index 0 so that index 1 will match week 1
    weekLinks.insert(0, "")
    for i in range(1, len(weekLinks)):
        print(i, ": ", weekLinks[i])
    print(weekLinks)

    return weekLinks


"""
    The purpose of getGameLinks is to get passed a link to a week and then navigate to the page and grab all of the 
    game links from the current week page.
"""
def getGameLinks(currentWeek):
    # for week in range(1, 23):
    # Navigate to the week
    driver.get(currentWeek)

    # Get all game links
    links = []
    gameLinks = driver.find_elements(By.LINK_TEXT, "Final")
    # Print / append each game link to the links list
    for link in gameLinks:
        links.append(link.get_attribute('href'))
        print(link.get_attribute('href'))
    print(links)

    return links


def scrapeSingleGame(link, week):
    ##################################### SINGLE GAME SCRAPE STARTS HERE ######################################
    # Navigate to the current game page
    driver.get(link)
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

    # Get the two teams into the teams list
    teams = []
    teams = getTeams(soup)

    allData = []
    # Create the CSV appending player IDs, snap counts, opposing team, and player stats
    for row in allRows:
        row_data = []

        for cell in row.findAll(["td", "th"]):
            row_data.append(cell.get_text())
            # print("ROW DATA: ", row_data)
            # Try to put the playerIDs in
            try:
                # Check if the rowData[0] player name matches the playerID name
                if row_data[0] == playerID[0]:
                    row_data.insert(1, playerID[1])
                    row_data.insert(4, week)
                    playerID.pop(0)
                    playerID.pop(0)
            except IndexError as e:
                pass
                #print("The index is out of range Idk if this is fine but w/e it works for now: ", e)

        # This tries to be the header in the file, but I don't want it, so I make it go to the next iteration
        if "Passing" in row_data or "Player" in row_data:
            continue

        for q in range(len(offensiveSnapCounts)):
            # print("ROW: ", row_data[0], " SNAP: ", offensiveSnapCounts[q][0])
            if row_data[0] == offensiveSnapCounts[q][0]:
                # print("BANNNNG")
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
        allData.append(rowData)
    return allData
    #####################################  SINGLE GAME SCRAPE ENDS HERE  ######################################


def getTeams(theSoup):
    # The teamList set holds the two teams who played, a set is used because there are going to be unneeded duplicates
    teamList = set()

    # Find the <div> element with id "div_player_offense" and get the <tbody> tag inside it
    player_offense_div = theSoup.find("div", {"id": "div_player_offense"})
    tbody = player_offense_div.find("tbody")

    # Find all <tr> tags in the <tbody> tag and get the team names from the "tm" column
    for tr in tbody.find_all("tr"):
        td = tr.find("td", {"data-stat": "team"})
        if td is not None:
            teamList.add(td.text.strip())

    # Convert the set back to a list so that everything back in the main code is using a list.
    teamList = list(teamList)

    return teamList


def scrapeFromCurrentWeek(curWeek, weekLinks):
    with open("testfile.csv", "a", newline="") as f:
            # Create the csv and make the header
            table_to_csv = csv.writer(f)
            header = ["Player", "PID", "Pos", "Week", "Tm", "Opp", "Cmp", "PassAtt", "PassYds", "PassTD", "Int", "Sacked",
                      "YardsLostSack", "PassLng", "Rate", "RushAtt",
                      "RushYards", "RushTD", "RushLng", "Tgt", "Rec", "RecYds", "RecTD", "RecLng", "Fmb", "FL", "Snap",
                      "Snap%"]

            for week in range(curWeek, len(weekLinks)):
            #for week in range(1, 23):
                # # Navigate to the week
                # driver.get(weekLinks[week])
                #
                # # Get all game links
                # links = []
                # gameLinks = driver.find_elements(By.LINK_TEXT, "Final")
                # # Print / append each game link to the links list
                # for link in gameLinks:
                #     links.append(link.get_attribute('href'))
                #     print(link.get_attribute('href'))
                # print(links)
                links = getGameLinks(weekLinks[week])

                # Get each game for that weeks stats
                for link in links:
                    print("Current game: ", link, " Current week: ", week)
                    #gameData = scrapeSingleGame(link, week)
                    #print(gameData)
                    ##################################### SINGLE GAME SCRAPE STARTS HERE ######################################
                    # Navigate to the current game page
                    driver.get(link)
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

                    # Get the two teams into the teams list
                    teams = []
                    teams = getTeams(soup)

                    # Create the CSV appending player IDs, snap counts, opposing team, and player stats
                    for row in allRows:
                        row_data = []

                        for cell in row.findAll(["td", "th"]):
                            row_data.append(cell.get_text())
                            # print("ROW DATA: ", row_data)
                            # Try to put the playerIDs in
                            try:
                                # Check if the rowData[0] player name matches the playerID name
                                if row_data[0] == playerID[0]:
                                    row_data.insert(1, playerID[1])
                                    row_data.insert(4, week)
                                    playerID.pop(0)
                                    playerID.pop(0)
                            except IndexError as e:
                                pass
                                #print("The index is out of range Idk if this is fine but w/e it works for now: ", e)

                        # This tries to be the header in the file, but I don't want it, so I make it go to the next iteration
                        if "Passing" in row_data or "Player" in row_data:
                            continue

                        for q in range(len(offensiveSnapCounts)):
                            # print("ROW: ", row_data[0], " SNAP: ", offensiveSnapCounts[q][0])
                            if row_data[0] == offensiveSnapCounts[q][0]:
                                # print("BANNNNG")
                                row_data.insert(2, offensiveSnapCounts[q][1])
                                # Append the number of snaps to the end of the players row
                                row_data.append(offensiveSnapCounts[q][2])
                                # Append the snap % to the end of the players row. regex is used because it comes in with %
                                snapPercent = re.sub("[^\d\.]", "", offensiveSnapCounts[q][3])
                                row_data.append(snapPercent)
                                #row_data.append(offensiveSnapCounts[q][3])

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

                        #print(row_data)
                        table_to_csv.writerow(row_data)

        #####################################  SINGLE GAME SCRAPE ENDS HERE  ######################################
    driver.quit()

def main():
    weekLinks = getWeekLinks()
    # for week in range(1, len(weekLinks)-1):
    #     driver.get(weekLinks[week])
    #     time.sleep(2)

    # # Get all game links
    # links = []
    # gameLinks = driver.find_elements(By.LINK_TEXT, "Final")
    # # Print / append each game link to the links list
    # for link in gameLinks:
    #     links.append(link.get_attribute('href'))
    #     print(link.get_attribute('href'))
    # print(links)

    # # navigate to each gamelink and get the PBP
    # for link in links:
    #     driver.get(link)
    #     # Get the entire page html
    #     theHtml = driver.page_source
    #     # Find the table using beautiful soup
    #     soup = BeautifulSoup(theHtml, "html.parser")
    #     pbpTable = soup.findAll(id="div_pbp")[0]
    #     # print(pbpTable)
    #     allRows = pbpTable.findAll("tr")
    #     # print(allRows)
    #     # Export to CSV
    #     with open("testfile.csv", "a", newline="") as f:
    #         table_to_csv = csv.writer(f)
    #         for row in allRows:
    #             row_data = []s
    #             for cell in row.findAll(["td", "th"]):
    #                 row_data.append(cell.get_text())
    #             table_to_csv.writerow(row_data)
    #         time.sleep(random.randint(5, 8))

    try:
        df = pd.read_csv('testfile.csv')
        maxWeek = max(df.Week)
        print(max(df.Week))
        print(type(df))
        if maxWeek < (len(weekLinks) - 1):
            print("need to scrape")
            return [int(maxWeek)+1, weekLinks]
            # scrapeFromCurrentWeek(maxWeek + 1, weekLinks)
        else:
            return "up to date"

    except: # if something goes wrong just remake the whole file
        #pass
        with open("testfile.csv", "w", newline="") as f:
            # Create the csv and make the header
            table_to_csv = csv.writer(f)
            header = ["Player", "PID", "Pos", "Week", "Tm", "Opp", "Cmp", "PassAtt", "PassYds", "PassTD", "Int", "Sacked",
                      "YardsLostSack", "PassLng", "Rate", "RushAtt",
                      "RushYards", "RushTD", "RushLng", "Tgt", "Rec", "RecYds", "RecTD", "RecLng", "Fmb", "FL", "Snap",
                      "Snap%"]
            table_to_csv.writerow(header)

            for week in range(1, len(weekLinks)):
            #for week in range(1, 23):
                # # Navigate to the week
                # driver.get(weekLinks[week])
                #
                # # Get all game links
                # links = []
                # gameLinks = driver.find_elements(By.LINK_TEXT, "Final")
                # # Print / append each game link to the links list
                # for link in gameLinks:
                #     links.append(link.get_attribute('href'))
                #     print(link.get_attribute('href'))
                # print(links)
                links = getGameLinks(weekLinks[week])

                # Get each game for that weeks stats
                for link in links:
                    print("Current game: ", link, " Current week: ", week)
                    #gameData = scrapeSingleGame(link, week)
                    #print(gameData)
                    ##################################### SINGLE GAME SCRAPE STARTS HERE ######################################
                    # Navigate to the current game page
                    driver.get(link)
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

                    # Get the two teams into the teams list
                    teams = []
                    teams = getTeams(soup)

                    # Create the CSV appending player IDs, snap counts, opposing team, and player stats
                    for row in allRows:
                        row_data = []

                        for cell in row.findAll(["td", "th"]):
                            row_data.append(cell.get_text())
                            # print("ROW DATA: ", row_data)
                            # Try to put the playerIDs in
                            try:
                                # Check if the rowData[0] player name matches the playerID name
                                if row_data[0] == playerID[0]:
                                    row_data.insert(1, playerID[1])
                                    row_data.insert(4, week)
                                    playerID.pop(0)
                                    playerID.pop(0)
                            except IndexError as e:
                                pass
                                #print("The index is out of range Idk if this is fine but w/e it works for now: ", e)

                        # This tries to be the header in the file, but I don't want it, so I make it go to the next iteration
                        if "Passing" in row_data or "Player" in row_data:
                            continue

                        for q in range(len(offensiveSnapCounts)):
                            # print("ROW: ", row_data[0], " SNAP: ", offensiveSnapCounts[q][0])
                            if row_data[0] == offensiveSnapCounts[q][0]:
                                # print("BANNNNG")
                                row_data.insert(2, offensiveSnapCounts[q][1])
                                # Append the number of snaps to the end of the players row
                                row_data.append(offensiveSnapCounts[q][2])
                                # Append the snap % to the end of the players row. regex is used because it comes in with %
                                snapPercent = re.sub("[^\d\.]", "", offensiveSnapCounts[q][3])
                                row_data.append(snapPercent)
                                #row_data.append(offensiveSnapCounts[q][3])

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

                        #print(row_data)
                        table_to_csv.writerow(row_data)

        #####################################  SINGLE GAME SCRAPE ENDS HERE  ######################################
    driver.quit()


if __name__ == "__main__":
    main()

###################################### SINGLE GAME SCRAPE STARTS HERE ######################################

# # Get the entire page html
# theHtml = driver.page_source
# # Find the table using beautiful soup
# soup = BeautifulSoup(theHtml, "html.parser")
# offenseTable = soup.findAll(id="div_player_offense")[0]
# allRows = offenseTable.findAll("tr")
#
# # Make a list of [player name, player ID]
# playerID = []
# for row in allRows:
#     # Get the player IDs from the table
#     for cell in row.findAll(["td", "th"]):
#         # Sometimes it grabs None types and puts them in the array, this just makes sure it doesn't do that.
#         if cell.get("data-append-csv") is not None:
#             playerID.append(cell.get_text())
#             playerID.append(cell.get("data-append-csv"))
#
# # print(allRows)
# # Export to CSV
# # with open("testfile2.csv", "a", newline="") as f:
# #     table_to_csv = csv.writer(f)
#
#
# # Make a list containing [Player, Pos, Num, Pct, Num, Pct, Num, Pct]
# homeSnapsTable = soup.findAll(id="home_snap_counts")[0]
# awaySnapsTable = soup.findAll(id="vis_snap_counts")[0]
# homeSnapsRows = homeSnapsTable.findAll("tr")
# awaySnapsRows = awaySnapsTable.findAll("tr")
# offensiveSnapCounts = []
# for row in homeSnapsRows:
#     rowData = []
#     # Get the single players name / position / snap counts / snap % and more into a list called rowData
#     for cell in row.findAll(["td", "th"]):
#         rowData.append(cell.get_text())
#     # rowData[1] is the position of the player in the table. This makes sure to print only offensive players
#     if rowData[1] in ["QB", "RB", "WR", "TE", "FB"]:
#         offensiveSnapCounts.append(rowData)
#
# for row in awaySnapsRows:
#     rowData = []
#     # Get the single players name / position / snap counts / snap % and more into a list called rowData
#     for cell in row.findAll(["td", "th"]):
#         rowData.append(cell.get_text())
#     # rowData[1] is the position of the player in the table. This makes sure to print only offensive players
#     if rowData[1] in ["QB", "RB", "WR", "TE", "FB"]:
#         offensiveSnapCounts.append(rowData)
#
# print(offensiveSnapCounts)
#
# for row in offensiveSnapCounts:
#     print("Name: ", row[0], "Pos: ", row[1])
#
# with open("testfile.csv", "w", newline="") as f:
#     # Create the csv and make the header
#     table_to_csv = csv.writer(f)
#     header = ["Player", "PID", "Pos", "Tm", "Cmp", "Att", "Yds", "TD", "Int", "Sk", "Yds", "Lng", "Rate", "Att", "Yds",
#               "TD", "Lng", "Tgt", "Rec", "Yds", "TD", "Lng", "Fmb", "FL", "Snap", "Snap%"]
#     table_to_csv.writerow(header)
#     # Create the CSV appending player IDs, snap counts, and player stats
#     for row in allRows:
#         row_data = []
#
#         for cell in row.findAll(["td", "th"]):
#             row_data.append(cell.get_text())
#             # Try to put the playerIDs in
#             try:
#                 # Check if the rowData[0] player name matches the playerID name
#                 if row_data[0] == playerID[0]:
#                     row_data.insert(1, playerID[1])
#                     playerID.pop(0)
#                     playerID.pop(0)
#             except IndexError as e:
#                 print("The index is out of range Idk if this is fine but w/e it works for now: ", e)
#
#         # This tries to be the header in the file, but I don't want it, so I make it go to the next iteration
#         if "Passing" in row_data or "Player" in row_data:
#             continue
#
#         # # Try to put the Position, and snap counts in
#         # try:
#         #     # Check if the row_data[0] player name matches the offensiveSnapCounts name
#         #     print("ROW DATA: ", row_data[0], " OSC: ", offensiveSnapCounts[0][0])
#         #     if row_data[0] == offensiveSnapCounts[0][0]:
#         #         row_data.insert(2, offensiveSnapCounts[0][1])
#         #         # Append the number of snaps to the endof the players row
#         #         row_data.append(offensiveSnapCounts[0][2])
#         #         # Append the snap % to the end of the players row
#         #         row_data.append(offensiveSnapCounts[0][3])
#         #         offensiveSnapCounts.pop(0)
#         #     # Create Pos, num, pct column if they aren't already
#         #     elif row_data[0] == "Player" and row_data[2] != "Pos" and row_data[24] != "Num" and row_data[25] != "Pct":
#         #         row_data.insert(2, "Pos")
#         #         row_data.append("Num")
#         #         row_data.append("Pct")
#         # except IndexError as e:
#         #     print("The index is out of range Idk if this is fine but w/e it works for now: ", e)
#         print(row_data)
#         table_to_csv.writerow(row_data)
#
#
# # Open the file and put in the snap counts number and %
# path = "testfile.csv"
# # Read in Data
# rows = []
# with open(path, newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         rows.append(row)
# # Edit the Data
# for i in range(1, len(rows)):
#     for q in range(len(offensiveSnapCounts)):
#         print("ROW: ", rows[i], " SNAP: ", offensiveSnapCounts[q][0])
#         if rows[i][0] == offensiveSnapCounts[q][0]:
#             print("BANNNNG")
#             rows[i].insert(2, offensiveSnapCounts[q][1])
#             # Append the number of snaps to the endof the players row
#             rows[i].append(offensiveSnapCounts[q][2])
#             # Append the snap % to the end of the players row
#             rows[i].append(offensiveSnapCounts[q][3])
#             break
#
# print(len(rows))
# # Write the Data to File
# with open(path, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(rows)
######################################  SINGLE GAME SCRAPE ENDS HERE  ######################################


# count = driver.find_element(By.LINK_TEXT, "Final")
# print("THERE")
# count.click()
# print("DEFF NOT")

# #Get play by play text
# pbp = driver.find_element(By.ID, "div_pbp")
# print(type(pbp))
# print(pbp.text)
#
# # Get the entire page html
# theHtml = driver.page_source
# #print(theHtml)
#
# # Find the table using beautiful soup
# soup = BeautifulSoup(theHtml, "html.parser")
# pbpTable = soup.findAll(id="div_pbp")[0]
# #print(pbpTable)
# allRows = pbpTable.findAll("tr")
# #print(allRows)
# for row in allRows:
#     row_data = []
#     for cell in row.findAll(["td", "th"]):
#         row_data.append(cell.get_text())
#     print(row_data)


# driver.get("file:///D:/PycharmProjects/NFLScraper/Wild%20Card%20-%20Seattle%20Seahawks%20at%20San%20Francisco%2049ers%20-%20January%2014th,%202023%20_%20Pro-Football-Reference.com.html")
# # with open('testfile.csv','w', newline='') as d:
# #   for row in pbp.text:
# #        csv.writer(d).writerow(["Quarter", "Time", "Down", "ToGo", "Location", "HOME", "AWAY", "DETAIL", "EPB", "EPA"])
# #search = driver.find_element(By.ID, "cookie")
# file_object = open('testfile.csv', 'r')
# first_table = driver.find_elements(By.XPATH,"//div[@id = 'div_pbp']//table[1]")
# for first in first_table:
#     print(first)
# file_object.close()
#
#
#
# for first in first_table:
#    print(first.text)
#    print("YO")


# #url_foot = "file:///D:/PycharmProjects/NFLScraper/Wild%20Card%20-%20Seattle%20Seahawks%20at%20San%20Francisco%2049ers%20-%20January%2014th,%202023%20_%20Pro-Football-Reference.com.html"
# response = "file:///D:/PycharmProjects/NFLScraper/Wild%20Card%20-%20Seattle%20Seahawks%20at%20San%20Francisco%2049ers%20-%20January%2014th,%202023%20_%20Pro-Football-Reference.com.html"
#
# #response = requests.get("https://www.pro-football-reference.com/boxscores/202301150buf.htm")
#
# url_foot = response.text
# #html_foot = urlopen(url_foot)
# print(url_foot)
# soup = BeautifulSoup(url_foot, "html.parser")
# first_table = soup.findAll(id="div_pbp")[0]
# print(first_table)
# all_rows = first_table.findAll("tr")
# with open("testfile.csv", "w", newline="") as f:
#     table_to_csv = csv.writer(f)
#     for row in all_rows:
#             row_data = []
#             for cell in row.findAll(["td", "th"]):
#                 row_data.append(cell.get_text())
#             table_to_csv.writerow(row_data)
#
# while(True):
#     pass
#     #search.click()

# driver.get("https://en.wikipedia.org/wiki/Main_Page")
#
# # count = driver.find_element(By.CSS_SELECTOR, "#articlecount a")
# # count.click()
#
# # allPortals = driver.find_element(By.LINK_TEXT, "English")
# # allPortals.click()
#
# search = driver.find_element(By.NAME, "search")
# search.send_keys("Python")
# search.send_keys(Keys.ENTER)
# print(count.text)
