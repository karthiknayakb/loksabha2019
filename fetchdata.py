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