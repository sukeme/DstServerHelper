# import sql_task
import json
import os
from sql_task import QueryMondInfo


li = []
aa = QueryMondInfo(0)


def upload_modinfo():
    with open(r'C:\Users\suke\Desktop\modinfo\v.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    v1 = data.get('v1')
    v2 = data.get('v2')
    num = 0
    for j, jj in [(1, v1), (2, v2)]:
        for i in jj:
            path = r'C:\Users\suke\Desktop\modinfo\mod ok'
            if os.path.exists(os.path.join(path, i + '.json')):
                with open(os.path.join(path, i + '.json'), 'r', encoding='utf-8') as ff:
                    info = ff.read()
            else:
                info = '{}'

            modinfo = {
                'mod_id': int(i),
                'update_time': jj.get(i).get('vt'),
                'check_time': 1644000000,
                'mod_type': j,
                'mod_info': info
            }
            num += 1
            li.append(modinfo)
            if len(li) == 100:
                print(num, (aa.add_data('modinfo', *li)))
                li.clear()
    if li:
        print(num, (aa.add_data('modinfo', *li)))
        li.clear()


upload_modinfo()
