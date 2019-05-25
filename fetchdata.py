import json
import requests
from bs4 import BeautifulSoup

url = "http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseU011.htm"

soup = BeautifulSoup(requests.get(url).content,"html.parser")

states = soup.find_all("input",{"type":"hidden"})
state_dict = {}
for state in states:
    if "value" in str(state):
        state_dict[state["id"]] = state["value"]
    else:
        pass

with open("states.json","w") as st:
    json.dump(state_dict,st)

urltemp = "http://results.eci.gov.in/pc/en/constituencywise/Constituencywise%s%s.htm?ac=%s"
#stateID,constituency,constituency
clinks = []
for state in state_dict:
    consti = state_dict[state].split(";")
    for c in consti:
        if c:
            cid = c.split(",")[0]
            clinks.append(urltemp%(state,cid,cid))
            
def getdata(url):
    