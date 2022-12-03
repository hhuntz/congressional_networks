'''
These functions expect you to have 2 data sources in a subdirectory called 'data'
    1. bill data in XML files via https://github.com/unitedstates/congress
        or from propublica @ https://www.propublica.org/datastore/dataset/congressional-data-bulk-legislation-bills
    2. data on Members of Congress from https://bioguide.congress.gov/search (download link in top right)
You can uncomment code in main() to save more files along the way
    Othwerwise, output is:
        edges.csv, with rows as edges and weights between id nums for MOCs w/ weights as # of cosponsorships
        moc_info.json, which contains info on each MOC by bioguide_id
'''

import json
import csv
import os

def get_sponsor_data():
    '''
    gets sponsor dict for ~324,000 total bills
    iterates through data in 'data' folder from 
    '''
    sponsor_dict = {}
    i = 0
    errors = 0
    for session in range(93, 117):
        sponsor_dict[session] = {}

        path = os.path.join(os.path.dirname(__file__), f'data/{str(session)}')

        for bill_type in os.listdir(path):
            if '.DS_Store' in bill_type:
                continue
            type_path = os.path.join(path, bill_type)
            for bill in os.listdir(type_path):
                bill_path = os.path.join(type_path, bill)
                if '.DS_Store' in bill_path:
                    continue
                try:
                    sponsor_dict[session][bill] = {}
                    data_path = bill_path + '/data.json'
                    with open(data_path, 'r') as f:
                        j = json.loads(f.read())
                        # get IDs for MOCs sponsoring the bill
                        try:
                            # older system was thomas id -- appending 't' at front
                            sponsor_dict[session][bill]['sponsor'] = j['sponsor']['thomas_id']   
                            sponsor_dict[session][bill]['cosponsors'] = [cosponsor['thomas_id'] for cosponsor in j['cosponsors']]
                        except: 
                            # newer system is bioguide id -- appending 'b' at front
                            sponsor_dict[session][bill]['sponsor'] = j['sponsor']['bioguide_id']   
                            sponsor_dict[session][bill]['cosponsors'] = [cosponsor['bioguide_id'] for cosponsor in j['cosponsors']]
                    
                    i += 1
                    if i % 1000 == 0:
                        print(f'{i} bills done') 

                except:
                    # errors seem to be bills without sponsor info (saved as 'null' in the json)
                    # error rate is about 1.5 in 10,000
                    errors += 1
                    print(f'skipped {bill} from {session} ------ {errors} errors')
                    
    return sponsor_dict

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

    edge_list = edges = [f'{k},{v}' for k,v in edge_dict.items()]
    print('done making edge list')
    return edge_list

def get_moc_dict():
    moc_dict = {}
    path = os.path.join(os.path.dirname(__file__), f'data/BioguideProfiles')
    for moc_file in os.listdir(path):
        data_path = path + '/' + moc_file
        with open(data_path, 'r') as f:
            j = json.loads(f.read())
        moc_dict[moc_file.replace('.json', '')] = j
    return moc_dict

def write_json(d, file_path):
    print('writing JSON file')
    with open(file_path, 'w+') as f:
        dict_str = json.dumps(d)
        f.write(dict_str)

def write_edge_csv(lst):
    print('writing csv file...')
    path = os.path.join(os.path.dirname(__file__), 'data/edges.csv')
    with open(path, 'w+') as f:
        for line in lst:
            f.write(f"{line}\n")
    print('all done!')


if __name__ == '__main__':
    sponsors = get_sponsor_data()
    # write_json(sponsors, 'data/sponsors.json')

    # with open('data/sponsors.json') as f:
    #     sponsors_json = f.read()
    # sponsors = json.loads(sponsors_json)

    edge_dict = get_edge_list(sponsors)
    write_edge_csv(edges)

    moc_info_path = os.path.join(os.path.dirname(__file__), f'data/moc_info.json')
    moc_dict = get_moc_dict()
    write_json(moc_dict, moc_info_path)
