from datetime import datetime

import pandas as pd

# CSV file path
csv_file_path = 'file.csv'

df = pd.read_csv(csv_file_path)
df['last_seen'] = df['last_seen'].fillna(pd.Timestamp('1970-01-01'))
df['last_seen'] = [datetime.fromtimestamp(x) for x in df['last_seen']]
df['fullname'] = df['fullname'].fillna('None').astype('string')
df['town'] = df['town'].fillna('None').astype('string')
df['contacts'] = df['contacts'].fillna('None').astype('string')

df.to_csv('file.csv', index=True)
