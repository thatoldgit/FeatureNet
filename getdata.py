import json
import requests

from igraph import *



with open('requestForm.json') as f:
   jsonBody = json.load(f)

print(jsonBody)

#g = Graph()

featuresBetweenRequest = requests.post('http://featurenet.zz-dev.de:8090/features/aggregated', json=jsonBody)

featureList = json.loads(featuresBetweenRequest.content)

print(featureList)
g = Graph()
g.add_vertices(len(featureList))

names = list()
ids = list()
amount = list()

counter = 0
for feature in featureList:
   #featuringArtistId = feature["artistId"]
   #featuringArtistName = feature["artistName"]
   artistFeatures = feature["features"]
   names.append(feature["artistName"])
   ids.append(feature["artistId"])

   #print(featuringArtistId, " ", artistFeatures)

   #TODO insert node for featuring artist if not existing

   #if g["artistId"] != null:
       #g.add(new Node("artistName))

   for featuredArtist in artistFeatures:
       featuredArtistId = featuredArtist["artistId"]
       v = g.vs.find("artistId" == featuredArtistId)
       #own = g.vs.find("artistId" == feature["artistId"])
       e = g.add_edge(counter, v)

       #e["width"] = featuredArtist["amount"]
       amount.append(featuredArtist["amount"])
       #TODO insert node for featured artist if not existing

       #if g["artistId"] != :
       # g.add(new Node("artistName))

       #TODO add edge from featuring artist to featured artist
   counter = counter + 1
       #g.add()
g.vs["label"] = names
g.vs["id"] = ids
g.es["width"] = amount
plot(g, "testneu1.png",
        layout=g.layout("kk"), directed=True,
        bbox=(2400, 1600), margin=100)


   # create Node for featuring artist if not existent ye

#   for featureLink in artistFeatures:
       #create node for featured artist if not existent yet
       #create edge for relation if not existent yet


# check if edge exists
# check if node exists