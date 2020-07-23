import mwclient
import time
import datetime as dt
from datetime import date, timedelta, datetime
import json


# All the data is taken from LoL Gamepedia's API, more info on it can be found at lol.gamepedia.com/Help:API_Documentation
# This scripts gets the match history up to one day before the day it's run and saves it in a json file.
# The raw match history then has to be fixed so that all the players have their most recent name.
# I still need to get around to doing that with the teams as well.


# This function takes a date as the input and outputs a list of the games that happened that day.
# The output is a list of dictionaries, each with the date, the tournament, the teams, the winner, the patch,
# the players on each team along with their role, champion, summoner spells, and keystone.
def getmh(date):
    site = mwclient.Site('lol.gamepedia.com', path='/')
    new_query = site.api('cargoquery',
    	limit = "500",
    	tables = "ScoreboardGames=SG, ScoreboardPlayers=SP",
        join_on = "SG.UniqueGame=SP.UniqueGame",
    	fields = "SG.Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SG.Patch, SP.Link, SP.Team, SP.Champion, SP.SummonerSpells, SP.KeystoneMastery, SP.KeystoneRune, SP.Role, SP.UniqueGame, SP.Side",
    	where = "SG.DateTime_UTC >= '" + str(date-dt.timedelta(days=1)) + "' AND SG.DateTime_UTC <= '" + str(date) + "'",
    	offset = "0"
    )

    ofst=500
    response={}
    response["cargoquery"]=[]
    while len(new_query["cargoquery"])!=0:
        response["cargoquery"]+=new_query["cargoquery"]
        new_query = site.api('cargoquery',
        	limit = "500",
        	tables = "ScoreboardGames=SG, ScoreboardPlayers=SP",
            join_on = "SG.UniqueGame=SP.UniqueGame",
        	fields = "SG.Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SG.Patch, SP.Link, SP.Team, SP.Champion, SP.SummonerSpells, SP.KeystoneMastery, SP.KeystoneRune, SP.Role, SP.UniqueGame, SP.Side",
        	where = "SG.DateTime_UTC >= '" + str(date-dt.timedelta(days=1)) + "' AND SG.DateTime_UTC <= '" + str(date) + "'",
        	offset = str(ofst)
        )
        ofst+=500

    mh=[]
    previousGame=""

    for i in response["cargoquery"]:

        if i["title"]["UniqueGame"]!=previousGame:
            previousGame=i["title"]["UniqueGame"]
            mh.append({})


            mh[-1]["Tournament"]=i["title"]["Tournament"]
            mh[-1]["Date"]=str(dt.datetime.strptime(i["title"]["DateTime UTC"], "%Y-%m-%d %H:%M:%S").date())
            mh[-1]["Team1"]=i["title"]["Team1"]
            mh[-1]["Team2"]=i["title"]["Team2"]
            mh[-1]["Winner"]=i["title"]["Winner"]
            mh[-1]["Patch"]=i["title"]["Patch"]
            mh[-1]["Team1Players"]={}
            mh[-1]["Team2Players"]={}

            mh[-1]["Team1Players"][i["title"]["Link"]]={}
            mh[-1]["Team1Players"][i["title"]["Link"]]["Role"]=i["title"]["Role"]
            mh[-1]["Team1Players"][i["title"]["Link"]]["Champion"]=i["title"]["Champion"]
            mh[-1]["Team1Players"][i["title"]["Link"]]["SummonerSpells"]=i["title"]["SummonerSpells"]
            if i["title"]["KeystoneMastery"]!="":
                mh[-1]["Team1Players"][i["title"]["Link"]]["KeystoneMastery"]=i["title"]["KeystoneMastery"]
            if i["title"]["KeystoneRune"]!="":
                mh[-1]["Team1Players"][i["title"]["Link"]]["KeystoneRune"]=i["title"]["KeystoneRune"]


        else:
            mh[-1]["Team" + i["title"]["Side"] + "Players"][i["title"]["Link"]]={}
            mh[-1]["Team" + i["title"]["Side"] + "Players"][i["title"]["Link"]]["Role"]=i["title"]["Role"]
            mh[-1]["Team" + i["title"]["Side"] + "Players"][i["title"]["Link"]]["Champion"]=i["title"]["Champion"]
            mh[-1]["Team" + i["title"]["Side"] + "Players"][i["title"]["Link"]]["SummonerSpells"]=i["title"]["SummonerSpells"]
            if i["title"]["KeystoneMastery"]!="":
                mh[-1]["Team" + i["title"]["Side"] + "Players"][i["title"]["Link"]]["KeystoneMastery"]=i["title"]["KeystoneMastery"]
            if i["title"]["KeystoneRune"]!="":
                mh[-1]["Team" + i["title"]["Side"] + "Players"][i["title"]["Link"]]["KeystoneRune"]=i["title"]["KeystoneRune"]



    return mh



games_between_saves=500

# Opens the match history it's gotten before and checks the date of the last game.
# If the match history is empty it starts at a date just before the first game recorded on gamepedia.
with open("RawMatchHistory.json", mode="r", encoding="utf8") as f:
    mh=json.load(f)
if len(mh)>0:
    day=dt.datetime.strptime(mh[-1]["Date"], "%Y-%m-%d")
else:
    day=dt.datetime.strptime("2011-06-18", "%Y-%m-%d")

# Gets all the games between the date of the last game and the date of the previous day the program is run.
Counter=0
while day<dt.datetime.now()-dt.timedelta(days=1):
    print(day.strftime("%Y-%m-%d"), ": ", len(mh))
    time.sleep(1)
    mh+=getmh(day)
    day=day+dt.timedelta(days=1)
    Counter+=1
    # Every once in a while the current progress is sorted and saved.
    if Counter%games_between_saves==0:
        sorted_mh=sorted(mh, key = lambda i: dt.datetime.strptime(i['Date'], "%Y-%m-%d"))
        with open("RawMatchHistory.json", mode="w", encoding="utf8") as f:
            json.dump(mh, f)


# Sorts the match history by date and saves.
sorted_mh=sorted(mh, key = lambda i: dt.datetime.strptime(i['Date'], "%Y-%m-%d"))
with open("RawMatchHistory.json", mode="w", encoding="utf8") as f:
    json.dump(sorted_mh, f)
