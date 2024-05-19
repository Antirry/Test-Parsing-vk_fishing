import csv
from datetime import datetime

from clickhouse_connect import get_client

from project._extract_config import Extract_from_Config

clickhouse_params = Extract_from_Config('_Config.ini', 'clickhouse')

client = get_client(**clickhouse_params.config)

def row_reader():
    try:
        client.command("""
            CREATE TABLE example_table
            (
                `id` UInt32,
                `fullname` String,
                `last_seen` String,
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

    with open('file.csv', encoding='utf-8') as iris_csv:
        for line in csv.DictReader(iris_csv):
            yield {
                'id': int(line['id']),
                'fullname': str(line['fullname']),
                'last_seen': str(datetime.fromtimestamp(int(line['last_seen']))),
                'town': str(line['town']),
                'contacts': str(line['contacts']),
                'friends_count': int(line['friends_count'])
            }

client.command("INSERT INTO example_table VALUES", (line for line in row_reader()))
