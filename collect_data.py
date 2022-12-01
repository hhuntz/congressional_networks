import os
# API Key for ProPublica: eEGHBzl0fTZ99JH0cOe2wTcoNWeaIgDpaSWeuG1n
    # can enter an MOC and get party and other info for MOCs
final_data = {}

for session in range(93, 117):
    final_data[session] = {}

    path = os.path.join(os.path.dirname(__file__), f'data/{str(session)}')

    for btype in os.listdir(path):
        if '.DS_Store' in btype:
            continue
        subpath = os.path.join(path, btype)
        if 'res' in btype:
            continue

        for file in os.listdir(subpath):
            
            billpath = os.path.join(subpath, file)

            if  os.path.isdir(billpath):
                try:
                    bill_num = billpath.strip('/')[-1]
                    final_data[session][bill_num]
                    with open(billpath, 'r') as f:
                        j = json.loads(f)



                    print(billpath)



                #     bd = prepare_bill(billpath, ses)
                #     if bd.get('summary') is not None and bd.get('text') is not None:
                #         final_dataset.append(bd)
            
                except:
                    print('nope')

    # with open('/data/final_data/final/final_data_{}.jsonl'.format(session), 'w') as f:
    #     writer = jsonlines.Writer(f)
    #     writer.write_all(final_dataset)
