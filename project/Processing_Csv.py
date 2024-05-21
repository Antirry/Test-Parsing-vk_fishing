from datetime import datetime

import pandas as pd

# CSV file path
csv_file_path = 'file.csv'


def check_date_format(date:str) -> bool:
    """Checking date format

    Args:
        date (str): date from csv

    Returns:
        bool: bool date format
    """
    if len(date.split('.')) == 3:
        return True
    else:
        return False


def add_zeros(date:str) -> str:
    """Add zero to date

    Args:
        date (str): date from csv

    Returns:
        str: day.month.year
    """
    day, month, year = date.split('.')
    day = day.zfill(2)
    month = month.zfill(2)
    return f"{day}.{month}.{year}"


df = pd.read_csv(csv_file_path)
df['last_seen'] = df['last_seen'].fillna(pd.Timestamp('1970-01-01'))
df['last_seen'] = [datetime.fromtimestamp(x) for x in df['last_seen']]
df['fullname'] = df['fullname'].fillna('None').astype('string')
df['town'] = df['town'].fillna('None').astype('string')
df['contacts'] = df['contacts'].fillna('None').astype('string')


df['bdate'] = df['bdate'].fillna('01.01.1700')

# Применяем функцию check_date_format к столбцу bdate
df['bdate_valid'] = df['bdate'].apply(check_date_format)

# Заменяем неверные значения в столбце bdate
df.loc[df['bdate_valid'] == False, 'bdate'] = '01.01.1700'

# Удаляем вспомогательный столбец
del df['bdate_valid']


# Применяем функцию add_zeros к столбцу 'bdate'
df['bdate'] = df['bdate'].apply(add_zeros)

df['bdate'] = pd.to_datetime(df['bdate'], format='%d.%m.%Y', errors='coerce')

df.to_csv(f'{datetime.now().date()}-file.csv', index=False)
