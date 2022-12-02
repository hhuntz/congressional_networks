import json

# nodes are legislator download from https://github.com/unitedstates/congress-legislators

with open('data/sponsors.json') as f:
    sponsors_json = f.read()
sponsors_dict = json.loads(sponsors_json)

edge_list = []
seen = 0
for congress in sponsors_dict: 
    for bill in congress:
        all_sponsors = [sponsor for sponsor in sponsors[bill][congress][cosponsor]]
        all_sponsors.append(sponsors[bill][congress][sponsor])
        for sponsor in all_sponsors:
            for sponsor2 in all_sponsors:
                if sponsor != sponsor2:
                    edge_list.append((sponsor, sponsor2))

        seen += 1
        if seen % 1000 == 0:
            print (f'{seen} bills done -- length of edge_list is {len(edge_list)}')


