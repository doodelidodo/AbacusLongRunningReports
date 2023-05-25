import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import datetime

# db_path = f'LongRuningReports.sqlite'
db_path = f'D:/Abacus/LongRuningReports/LongRuningReports.sqlite'
conn = sqlite3.connect(db_path)

# Load data from the 'LongRuningReports' table into a Pandas DataFrame
df = pd.read_sql_query('SELECT * FROM LongRuningReports', conn)
# Close the SQLite connection
conn.close()

df = df.loc[df["done"] > 0]

current_date = datetime.datetime.now()
current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Name des PDF-Dateinamens mit Zeitstempel
pdf_filename = f"D:/Abacus/LongRuningReports/Auswertung/LongRunningReports_{current_timestamp}.pdf"
# pdf_filename = f'C:/Users/medo/Documents/coding/LongRunningReports/AbacusLongRunningReports/Auswertung/LongRunningReports_{current_timestamp}.pdf'

# Zeitstempel-String der letzten 2 Wochen berechnen
two_weeks_ago = current_date - datetime.timedelta(weeks=2)
timestamp_string = two_weeks_ago.strftime('%Y-%m-%d')

# Filtern des DataFrames basierend auf dem Zeitstempel
filtered_df = df[df['TimeStamp'] >= timestamp_string]

# Funktion zur Umrechnung der Zeitangabe in Sekunden
def time_to_seconds(time_string):
    minutes, seconds_mill = time_string.split(":")
    seconds = seconds_mill.split(".")[0]
    milliseconds = seconds_mill.split(".")[1]
    total_seconds = int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
    return total_seconds

# Umwandeln der Zeitangaben in Sekunden
filtered_df["Run"] = filtered_df["Run"].apply(time_to_seconds)

# Gruppieren und Durchschnitt berechnen
grouped_df = filtered_df.groupby('Report').mean()

# Sortieren und Top 10 auswählen
top_10_reports = grouped_df.nlargest(20, 'Run')

# Bar-Plot erstellen
plt.figure(figsize=(12, 6))
bars = plt.bar(top_10_reports.index, top_10_reports['Run'])

# Werte für jeden Balken anzeigen
for bar in bars:
    value = bar.get_height()
    minutes = int(value // 60)
    seconds = int(value % 60)
    label = f"{minutes:02d}:{seconds:02d}"
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label,
             ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
plt.xlabel('Report')
plt.ylabel('Durchschnittliche Laufzeit (Run)')
plt.title('Top 20 Reports mit der längsten durchschnittlichen Laufzeit')
plt.tight_layout()
plt.savefig(pdf_filename, format='pdf')