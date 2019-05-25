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
    soup = BeautifulSoup(requests.get(url).content,"html.parser")
    table = soup.find("table",{"class","table-party"})
    c_data = {}
    c_data["constituency"] = table.find("tr").text.strip()
    c_data["url"] = url
    headings = []
    for h in table.find("tr",{"style":"height: 20px; background-color: #FFC0CD; color:Black;"}).find_all("th"):
        headings.append(h.text.strip())
    
    trs = table.find_all("tr")[3:]
    candidates = trs[:-1]
    candidates_dict = []
    for candidate in candidates:
        data = []
        for d in candidate.find_all("td"):
            data.append(d.text.strip())
        candidates_dict.append(dict(zip(headings,data)))
    c_data["candidates"] = candidates_dict
    return c_data

results = []

count = 1
for link in clinks:
    print("Fetching(%s): %s"%(count,link))
    count = count+1
    results.append(getdata(link))
    
with open("results.json","w") as res:
    res.write("[\n")
    res.write(",\n".join(list(map(json.dumps,results))))
    res.write("]")