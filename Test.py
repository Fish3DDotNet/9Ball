
import pandas as pd
import os
import json
f = open("/static/data/Scorecard.json")
data = json.load(f)
f.close()
score = 19
sl = 5
print(str(data[str(sl)][str(score)]["w"])+ "-" +str(data[str(sl)][str(score)]["l"]))








t =True
if t == False:


    df1 = pd.read_excel("players.xlsx",engine='openpyxl')
    players = {"team1": {}, "team2": {}}

    for i in range(len(df1.Name1.values)):

        print(df1.Name1.values[i]+" "+str(df1.Player1.values[i])+" "+str(df1.SL1.values[i]))

        newplayer = {df1.Name1.values[i]:{"sl": df1.SL1.values[i], "p#": df1.Player1.values[i]}}
        players["team1"].update(newplayer)

    for i in range(len(df1.Name2.values)):

        print(df1.Name2.values[i]+" "+str(df1.Player2.values[i])+" "+str(df1.SL2.values[i]))

        newplayer = {df1.Name2.values[i]:{"sl": df1.SL2.values[i], "p#": df1.Player2.values[i]}}
        players["team2"].update(newplayer)
    
