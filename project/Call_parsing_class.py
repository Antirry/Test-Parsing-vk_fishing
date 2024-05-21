from time import sleep

import pandas as pd
from Parsing_vk_OOP import Parsing_Group_VK


def params() -> dict:
    from _extract_config import Extract_from_Config
    params = Extract_from_Config('_Config.ini', 'vk_api').config

    return params


data_vk_api = Parsing_Group_VK(params())

df = pd.DataFrame(pd.DataFrame(), columns=[
    'id',
    'fullname',
    'last_seen',
    'town',
    'contacts',
    'friends_count',
    'bdate'])
df.to_csv('file.csv', encoding='utf-8', index=False)

count_loop = int(data_vk_api._count_members() / 1000) +1

for i in range(0, count_loop):
    data_user = data_vk_api.members_from_group(i)
    sleep(0.5)
    data_user = [[
        x.get('id', 0),
        x.get('first_name', '') + ' ' + x.get('last_name', ''),
        int(x.get('last_seen', {}).get('time', 0)),
            # Using get method to avoid KeyError
        str(x.get('city', {}).get('title', None)),
            # Using get method to avoid KeyError
        str(x.get('mobile_phone', x.get('home_phone', None))),
            # Using get method to avoid KeyError
        data_vk_api._count_friends(x['id']),
        x.get('bdate', 0)
    ] for x in data_user]

    df = pd.DataFrame(data_user, columns=['id',
                                        'fullname',
                                        'last_seen',
                                        'town',
                                        'contacts',
                                        'friends_count',
                                        'bdate'])
    df.to_csv('file.csv', mode='a', encoding='utf-8', index=False, header=False)

    print('1000 записей готова!')
    sleep(5)
