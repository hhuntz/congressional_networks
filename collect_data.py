import os
import json

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
                        sponsor_dict[session][bill]['sponsor'] = 't' + j['sponsor']['thomas_id']   
                        sponsor_dict[session][bill]['cosponsors'] = ['t' + cosponsor['thomas_id'] for cosponsor in j['cosponsors']]
                    except: 
                        # newer system is bioguide id -- appending 'b' at front
                        sponsor_dict[session][bill]['sponsor'] = 'b' + j['sponsor']['bioguide_id']   
                        sponsor_dict[session][bill]['cosponsors'] = ['b' + cosponsor['bioguide_id'] for cosponsor in j['cosponsors']]
                
                i += 1
                if i % 1000 == 0:
                    print(f'{i} bills done') 

            except:
                # errors seem to be bills without sponsor info (saved as 'null' in the json)
                # error rate is about 1.5 in 10,000
                # ~324,000 total bills
                errors += 1
                print(f'skipped {bill} from {session} ------ {errors} errors')
                
print('writing JSON file')
with open('data/sponsors.json', 'w+') as f:
    dict_str = json.dumps(sponsor_dict)
    f.write(dict_str)
