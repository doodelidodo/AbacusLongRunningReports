# AbacusLongRunningReports
 Log Analyse von Long running Reports im Abacus

Wenn ein Report im Abacus länger läuft als er sollte, wird er im Abacus as long running report gelogged. Diese Logs liegen im folgenden Ordner: abac\log\abaengine\long_running_reports

Dieses Script exportiert ein Excel mit den wichtigsten Infos aus den Logs:
- Zeitstempel, wann dieses Log angelegt wurde
- User der den Report ausgeführt hat
- Reportname und den Pfad zum Report
- Ob der Report auch vollständig geladen wurde
- Anzahl finds die auf der DB abgesetzt wurden
- Anzahl rows
- Prozent welche durch Kriterien gefiltert werden
- Zeit die der Report benötigt hat, um die Daten zu laden

Wenn der Report nicht durchgelaufen ist, bekommt das Attribut done den Wert 0. Zudem werden dann die Attribute run und finds nicht abgefüllt.

Um das Script korrekt auszuführen, muss der Ordner von den long running reports in der variable "log_files_path" angepasst werden.