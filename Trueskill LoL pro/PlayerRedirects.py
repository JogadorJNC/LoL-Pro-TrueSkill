import mwclient
import json
import time

# Gets the player redirects and saves them.
# All the data is taken from LoL Gamepedia's API, more info on it can be found at lol.gamepedia.com/Help:API_Documentation

def getPlayerRedirects():

    os=0
    site = mwclient.Site('lol.gamepedia.com', path='/')
    response = site.api('cargoquery',
    	limit = "500",
        offset= os,
    	tables = "PlayerRedirects=PR",
    	fields = "PR.AllName, PR._pageName=Page",
    )

    ret={}

    for i in response["cargoquery"]:
        ret[i["title"]["AllName"]]=i["title"]["Page"]

    while len(response["cargoquery"])>0:
        os+=500
        time.sleep(1)
        site = mwclient.Site('lol.gamepedia.com', path='/')
        response = site.api('cargoquery',
        	limit = "500",
            offset= os,
        	tables = "PlayerRedirects=PR",
        	fields = "PR.AllName, PR._pageName=Page",
        )

        for i in response["cargoquery"]:
            ret[i["title"]["AllName"]]=i["title"]["Page"]

        print(os)
    return ret

pr_dict=getPlayerRedirects()

with open("PlayerRedirects.json", mode="w", encoding="utf8") as f:
    json.dump(pr_dict, f)
