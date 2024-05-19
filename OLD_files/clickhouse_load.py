from datetime import datetime

import pandas as pd
from clickhouse_connect import get_client

from project._extract_config import Extract_from_Config

clickhouse_params = Extract_from_Config('_Config.ini', 'clickhouse')

client = get_client(**clickhouse_params.config)
try:
    client.command("""
    CREATE TABLE example_table
    (
        `id` UInt32,
        `fullname` String,
        `last_seen` datetime64,
        `town` String,
        `contacts` String,
        `friends_count` UInt16
    )
    ENGINE = MergeTree
    PRIMARY KEY (id)
    ORDER BY (id)
    """)
except Exception:
    print('Таблица уже существует')

# CSV file path
csv_file_path = 'file.csv'

df = pd.read_csv(csv_file_path)
df['last_seen'] = df['last_seen'].fillna(pd.Timestamp('1970-01-01'))
df['last_seen'] = [datetime.fromtimestamp(x) for x in df['last_seen']]
df['fullname'] = df['fullname'].fillna('').astype('string')
df['town'] = df['town'].fillna('').astype('string')
df['contacts'] = df['contacts'].fillna('').astype('string')

client.insert('example_table', df)
