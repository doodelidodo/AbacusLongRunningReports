import os
import datetime
import pandas as pd
import sqlite3 as s3

# log_files_path = 'C:/Users/medo/Documents/coding/LongRunningReports/AbacusLongRunningReports/reports/'
log_files_path = 'D:/Abacus/abac/log/abaengine/long_running_reports/'

db_path = r"D:\Abacus\LongRuningReports\LongRuningReports.sqlite"
conn = s3.connect(db_path)

today_date = datetime.datetime.today().strftime('%Y-%m-%d')
all_reports = [f for f in os.listdir(log_files_path) if os.path.isfile(os.path.join(log_files_path, f)) and datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(log_files_path, f))).strftime('%Y-%m-%d') == today_date]

df = pd.DataFrame()

for report in all_reports:
    file = log_files_path + report
    f = open(file, 'r', encoding='utf-8')
    content_full = f.read()
    content = content_full.split()
    content_lines = content_full.split('\n')
    digit_lines = []
    f.close()

    for line in content_lines:
        if len(line) > 0:
            if line[0].isdigit():
                digit_lines.append(line)
                
    digit_lines_last = digit_lines[-1]

    def find_key_word(type):
        try: 
            if type == 'run':
                return digit_lines_last.split(': done')[0]
            if type == 'rows':
                return int(digit_lines_last.split('(')[1].split(',')[1].split(' = ')[1].replace('\'', ''))
            if type == 'criteria':
                return digit_lines_last.split('(')[1].split(',')[3].split(' = ')[1][:-1]
            if type == 'finds':
                return int(digit_lines_last.split('(')[1].split(',')[2].split(' = ')[1].replace('\'', ''))
            else:
                return ''
        except:
            return ""

    done = 0
    run = ''
    finds = ''
    rows = ''
    criteria = ''

    if 'done =>' in digit_lines_last:
        done = 1
        run = find_key_word('run')
        finds = find_key_word('finds')
        rows = find_key_word('rows')
        criteria = find_key_word('criteria')
        

    user = content[0][:-1]

    try: 
        report_name = [i for i in content_lines if "[D:" in i][0].split('[')[0]
        report_path =  [i for i in content_lines if "[D:" in i][0].split('[')[1][:-1]
    except:
        ""
        
    creation_timestamp = os.path.getmtime(file)
    creation_date_time= datetime.datetime.fromtimestamp(creation_timestamp)
    new_entry = {
        'TimeStamp': [creation_date_time], 
        'User': [user], 
        'Report': report_name, 
        'ReportPfad': [report_path], 
        'done': done, 
        'Finds': [finds], 
        'Rows': [rows], 
        'Kriterien': [criteria], 
        'Run': [run]
        }
    df_new_entry = pd.DataFrame(new_entry)
    df = pd.concat([df, df_new_entry])

df = df[~df['ReportPfad'].str.endswith('preview1.avx')]
df['ReportTyp'] = df['ReportPfad'].str.rsplit('.', 1).str[-1]

if not df.empty:
    df.to_sql("LongRuningReports", con=conn, if_exists='append', index=False, chunksize=1000)
    conn.close()
else:
    print('dataframe is empty')
    conn.close()
