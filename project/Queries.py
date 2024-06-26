#     !pip install ipykernel
#     !pip install pandas
#     !pip install requests
#     !pip install clickhouse_connect
#     !pip install plotly
#     !pip install --upgrade nbformat

from datetime import datetime

import pandas as pd
import plotly.express as px
from _extract_config import Extract_from_Config
from clickhouse_connect import get_client

clickhouse_params = Extract_from_Config('_Config.ini', 'clickhouse')

client = get_client(**clickhouse_params.config)

# print(client.command('SELECT * FROM Group_Members.example_table LIMIT 10'))

def Create_DataFrames(query: str, lst_names_col: list[str], split_by: str = "~"):
    data = \
        [x.split(split_by) \
        for x in split_by.join(query).split('\n')]
    df = pd.DataFrame(data, columns=lst_names_col)

    return df



# 'Количество повторов имен'

query = client.command("""
        SELECT names, COUNT(names) AS cnt_names
        FROM
        (
            SELECT SUBSTRING_INDEX(fullname, ' ', 1) AS names
            FROM Group_Members.example_table
        ) as t1
        GROUP BY names
        ORDER BY cnt_names DESC
        LIMIT 5;
""")

df = Create_DataFrames(query, ['names', 'cnt_names'])
df = df.sort_values('cnt_names')

fig = px.line(df,
             x='names',
             y='cnt_names',
             title='Количество повторов имен',
             template='plotly_dark',
             markers=True
)

fig.show()



# 'Последний онлайн (Кол-во друзей)'

query = client.command("""
    SELECT bdate, friends_count FROM Group_Members.example_table
    WHERE friends_count != 0 AND bdate != '1700-01-01'
""")

df = Create_DataFrames(query, ['bdate', 'friends_count'])

df['bdate'] = pd.to_datetime(df['bdate'])

today = datetime.today()
df['years_from_bdate'] = round((today - df['bdate']).dt.days / 365, 0)
df['years_from_bdate'] = df['years_from_bdate'].astype(int)
df['friends_count'] = df['friends_count'].astype(int)

df = df.sort_values('friends_count', ascending=False)

fig = px.scatter(df,
                x='years_from_bdate',
                y='friends_count',
                title='Последний онлайн (Кол-во друзей)',
                template='plotly_dark'
)

fig.show()



# ТОП 3 Города среднее количество друзей наибольшее

query = client.command("""
    SELECT town, ROUND(AVG(CASE WHEN friends_count != 0 THEN friends_count END), 2)
    AS avg_friends
    FROM Group_Members.example_table
    GROUP BY town
    ORDER BY avg_friends DESC
    LIMIT 3;
""")

df = Create_DataFrames(query, ['town', 'avg_friends'])
df = df.sort_values('avg_friends')

print(df)

"""
     town avg_friends
2  Гурзуф        4990
1   Ливны        6096
0   Россь        8056
"""



# Самый частый город среди участников

query = client.command("""
    SELECT town FROM (
        SELECT COUNT(id) AS cnt_ids, town FROM Group_Members.example_table
        WHERE town IN (SELECT town FROM
            (
                SELECT town,
                    ROUND(AVG(CASE WHEN friends_count != 0 THEN friends_count END), 2)
                    AS avg_friends
                FROM Group_Members.example_table
                GROUP BY town
                ORDER BY avg_friends DESC
                LIMIT 3
            ) as t1
        )
        GROUP BY town
        ORDER BY cnt_ids DESC
        LIMIT 1
    ) as t2;
""")

print(query)


"""
Ливны
"""
