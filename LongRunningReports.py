import os
import datetime
import pandas as pd

all_reports = os.listdir('reports/')
df = pd.DataFrame()

log_files_path = 'D:/Abacus/abac/log/abaengine/long_running_reports/'

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
            else:
                return int(digit_lines_last.split('(')[1].split(',')[2].split(' = ')[1].replace('\'', ''))
        except:
            return ""

    done = 0
    run = ''
    finds = ''
    if 'done =>' in digit_lines_last:
        done = 1
        run = find_key_word('run')
        finds = find_key_word('finds')
        

    user = content[0][:-1]

    try: 
        report_name = [i for i in content_lines if "[D:" in i][0].split('[')[0]
        report_path =  [i for i in content_lines if "[D:" in i][0].split('[')[1][:-1]
    except:
        ""
    creation_timestamp = os.path.getmtime(file)
    creation_date_time= datetime.datetime.fromtimestamp(creation_timestamp)
    new_entry = {'ErstellungsDatum': [creation_date_time], 'User': [user], 'Report': report_name, 'ReportPfad': [report_path], 'done': done, 'Finds': [finds], 'Run': [run]}
    df_new_entry = pd.DataFrame(new_entry)
    df = pd.concat([df, df_new_entry])

file_name =  "longRunningReportsAnalsyse.xlsx"
df.to_excel(file_name, index=False, engine="xlsxwriter")
