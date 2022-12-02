import json
import csv

# nodes are legislator download from https://github.com/unitedstates/congress-legislators

def get_edge_list(sponsors_dict):
    edge_dict = {}
    seen = 0
    errors = 0
    for congress in sponsors_dict: 
        for bill in sponsors_dict[congress]:
            try:
                all_sponsors = [sponsor for sponsor in sponsors[congress][bill]['cosponsors']]
                all_sponsors.append(sponsors[congress][bill]['sponsor'])
                for sponsor in all_sponsors:
                    for sponsor2 in all_sponsors:
                        if sponsor != sponsor2:
                            k = f'{sponsor},{sponsor2}'
                            edge_dict[k] = edge_dict.get(k, 0) + 1
            except:
                # errors are bills with sponsor and no co-sponsors
                    # no co-sponsors sometimes an empty list
                errors += 1
                print(f'skipped {bill} from {congress} ------ {errors} errors')

            seen += 1
            if seen % 1000 == 0:
                print (f'{seen} bills done -- length of edge_list is {len(edge_dict)}')
    print('done making edge list')
    return edge_dict

def write_edge_csv(lst):
    print('writing csv file...')
    with open('data/edges.csv', 'w+') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(lst)

    print('all done!')

if __name__ == '__main__':
    with open('data/sponsors.json') as f:
        sponsors_json = f.read()
    sponsors = json.loads(sponsors_json)
    edge_dict = get_edge_list(sponsors)
    edges = ['{k},{v}' for k,v in edge_dict.items()]
    write_edge_csv(edges)
