import json
import csv


#looping through the json and csv files
#this is super slow. sorry. it works though.
with open('parcel.json','r') as parcels:
    j = json.load(parcels)

auction_lines = []
with open('2013AuctionResults.csv','r') as auction:
    reader = csv.DictReader(auction)
    for line in reader:
        auction_lines.append(line)

cleaned_json = {"type":"FeatureCollection","features":[]}

i = 0
for f in j['features']:
    if i%100==0:
        print(i)
    i+=1
    properties = f["properties"]
    p = {"TAG":properties["TAG"],
         "BLOCKLOT":properties["BLOCKLOT"],
         "FULLADDR":properties["FULLADDR"],
         "PIN":properties["PIN"].strip()}
    for line in auction_lines:
        if line["Block"].strip()+line["Lot"].strip() == p["PIN"]:
            p.update(line)
            f["properties"] = p
            cleaned_json["features"].append(
                        {"type":"Feature",
                          "properties":p,
                          "geometry":f["geometry"]})
            break
print(len(cleaned_json["features"]))


with open('full_data.json','w') as outfile:
    json.dump(cleaned_json,outfile,indent=2)

