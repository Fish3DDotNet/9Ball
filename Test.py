
import pandas as pd
import os
import json

import csv


# defining the function to convert CSV file to JSON file
def convjson(csvFilename):
    # creating a dictionary
    teams = {}
    t = {}
    p = {}
    # reading the data from CSV file
    with open(csvFilename, encoding='utf-8') as csvfile:
        def row_count(filename):
            with open(filename) as in_file:
                return sum(1 for _ in in_file)

        csvRead = csv.DictReader(csvfile)
        last_line_number = row_count(csvFilename)
        team = "0"
        # Converting rows into dictionary and adding it to data
        for rows in csvRead:
            if rows["Team"] != team:
                if team == "0":
                    team = rows["Team"]
                    t = {rows["Team"]:{}}
                    t[rows["Team"]].update({rows["name"]: {"no":rows["no"],"sl": rows["sl"]}})
                elif rows["Team"] != team:
                    teams.update(t)
                    team = rows["Team"]
                    t = {rows["Team"]: {}}
                    t[rows["Team"]].update({rows["name"]: {"no": rows["no"], "sl": rows["sl"]}})
                else:
                    pass
            else:
                t[rows["Team"]].update({rows["name"]: {"no":rows["no"],"sl": rows["sl"]}})
                if last_line_number == 2:
                    teams.update(t)
            last_line_number -= 1

    return teams
csvFilename = r'teams.txt'


# Calling the convjson function
teams = convjson(csvFilename)

teamlist = []
print(teams.keys())

for i in teams.keys():
    print("Team : " + i)
    for x in teams[i].keys():
        print(x + " - " + teams[i][x]["no"] + " - " + teams[i][x]["sl"])



pass



# with open("teams.txt", "r") as f:
#     reader = csv.reader(f, delimiter="\t")
#     for i, line in enumerate(reader):
#         print('line[{}] = {}'.format(i, line))


# f = open("/static/data/Scorecard.json")
# data = json.load(f)
# f.close()
# score = 19
# sl = 5
# print(str(data[str(sl)][str(score)]["w"])+ "-" +str(data[str(sl)][str(score)]["l"]))


# t =True
# if t == False:
#
#
#     df1 = pd.read_excel("players.xlsx",engine='openpyxl')
#     players = {"team1": {}, "team2": {}}
#
#     for i in range(len(df1.Name1.values)):
#
#         print(df1.Name1.values[i]+" "+str(df1.Player1.values[i])+" "+str(df1.SL1.values[i]))
#
#         newplayer = {df1.Name1.values[i]:{"sl": df1.SL1.values[i], "p#": df1.Player1.values[i]}}
#         players["team1"].update(newplayer)
#
#     for i in range(len(df1.Name2.values)):
#
#         print(df1.Name2.values[i]+" "+str(df1.Player2.values[i])+" "+str(df1.SL2.values[i]))
#
#         newplayer = {df1.Name2.values[i]:{"sl": df1.SL2.values[i], "p#": df1.Player2.values[i]}}
#         players["team2"].update(newplayer)
    
