import json

# This scripts changes the player names to their most recent one.

# Open the files
with open("RawMatchHistory.json", mode="r", encoding="utf8") as f:
    mh=json.load(f)
with open("PlayerRedirects.json", mode="r", encoding="utf8") as f:
    pr=json.load(f)



pr_lower={}
for i in pr:
    pr_lower[i.lower()]=pr[i].lower()

oldPlayerNames=["","","","",""]
newPlayerNames=["","","","",""]

for i in mh:
    c=0
    for ii in i["Team1Players"]:
        oldPlayerNames[c]=ii
        if ii.lower() in pr_lower:
            newPlayerNames[c]=pr_lower[ii.lower()]
        else:
            newPlayerNames[c]=ii.lower()
        c+=1

    for ii in range(5):
        i["Team1Players"][newPlayerNames[ii]]=i["Team1Players"][oldPlayerNames[ii]]
        if (newPlayerNames[ii]!=oldPlayerNames[ii]):
            i["Team1Players"].pop(oldPlayerNames[ii], None)

for i in mh:
    c=0
    for ii in i["Team2Players"]:
        oldPlayerNames[c]=ii
        if ii.lower() in pr_lower:
            newPlayerNames[c]=pr_lower[ii.lower()]
        else:
            newPlayerNames[c]=ii.lower()
        c+=1

    for ii in range(5):
        i["Team2Players"][newPlayerNames[ii]]=i["Team2Players"][oldPlayerNames[ii]]
        if (newPlayerNames[ii]!=oldPlayerNames[ii]):
            i["Team2Players"].pop(oldPlayerNames[ii], None)




with open('FixedMatchHistory.json', mode='w', encoding="utf8") as f:
    json.dump(mh, f)
