
import pandas as pd
import os
import json

import csv

session = {}
context = {}
txt = ""

session['player1'] = 1
session['player2'] = "2"
session['player3'] = 3


for key in session:
    context[key] = session[key]


print(context)

#     hs = open("hst.txt", "a")
#     hs.write(key+" {session['"+key+"']: session["+key+"]}\n")
#     hs.close()
#
# d = {}
# with open("hst.txt") as f:
#     for line in f:
#         line = line.replace('"','')
#         (key, val) = line.split()
#         d[(key)] = val



