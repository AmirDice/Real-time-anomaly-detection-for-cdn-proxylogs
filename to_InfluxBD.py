import pandas as pd
# import json
from influxdb import DataFrameClient

dbhost = 'localhost'
dbport = 8086
dbuser = 'changeme'
dbpasswd = 'changeme'
dbname = 'project1db'
protocol = 'line'

# Define fields

Fields = ['timestamp', 'Status_code', 'contenttype', 'timefirstbyte', 'timetoserv', 'maxage',
          'path', 'geo_location', 'Host', 'hit']

# Define tag fields
datatags = ['contenttype', 'timefirstbyte', 'timetoserv', 'maxage', 'path', 'geo_location', 'Host', 'hit']

fixtags = {'ptcol': 'HTTP/1.1'}

# Read data without index of parse 'TimeStamp' and date

df = pd.read_csv(r"D:/source/repos/dara.csv", sep=',', index_col=False, parse_dates=['timestamp'], usecols=Fields)

# set TimeStamp field as index of DataFrame.
df.set_index('timestamp', inplace=True)

print(df.head(20))

client = DataFrameClient(dbhost, dbport, dbuser, dbpasswd, dbname)
# write data to project1.

client.write_points(df, "Project1db", tags=fixtags, tag_columns=datatags, protocol=protocol)
