import pandas as pd
import sqlite3

conn = sqlite3.connect('LongRuningReports.sqlite')

# Load data from the 'my_table' table into a Pandas DataFrame
df = pd.read_sql_query('SELECT * FROM LongRuningReports', conn)
# Close the SQLite connection
conn.close()

print(df)