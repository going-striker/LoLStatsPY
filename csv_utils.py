import csv
import time
from get_champions import get_champions
from get_champions_counters import get_champion_counters


def write_csv_champions(lane):
    champions = get_champions(lane)
    rows = list()
    for champ in champions:
        name = list()
        name.append(champ)
        rows.append(name)
    with open("champions_{}.csv".format(lane), "w", newline='') as f: 
        write = csv.writer(f) 
        write.writerows(rows) 
    
def read_csv_champions(lane):
    file = open("champions_{}.csv".format(lane), "r")
    champions = list(csv.reader(file, delimiter=","))
    file.close()
    result = list()
    for champ in champions:
        result.append(champ[0])
    return result

def write_csv_champion_counters(champion, lane):
    counters = get_champion_counters(champion, lane)
    rows = list()
    for champ in counters:
        row = list()        
        row.append(champ)
        row.append(counters[champ][0])
        row.append(counters[champ][1])
        rows.append(row)
    with open("matchups/counters_{}_{}.csv".format(lane, champion), "w", newline='') as f: 
        write = csv.writer(f) 
        write.writerows(rows) 

def read_csv_champion_counters(champion, lane):
    file = open("matchups/counters_{}_{}.csv".format(lane, champion), "r")
    counters = list(csv.reader(file, delimiter=","))
    file.close()
    result = dict()
    for champ in counters:
        result[champ[0]] = (champ[1], champ[2])
    return result


#champ_formatted = [champ[0].replace(".", "").replace(" ", "").replace("'", "").lower(), float(champ[1].replace("%", "")), int(champ[2].replace(",", ""))]
# champions_formatted = [x.replace(".", "").replace(" ", "").replace("'", "").lower() for x in champions]

champions = read_csv_champions("top")
champions_formatted = [x.replace(".", "").replace(" ", "").replace("'", "").lower() for x in champions]
global_counters = dict()
for x in champions_formatted:
    counters = read_csv_champion_counters(x, "top")
    counters_formatted = dict()
    for y in counters:
        counters_formatted[y.replace(".", "").replace(" ", "").replace("'", "").lower()] = (float(counters[y][0].replace("%", "")), int(counters[y][1].replace(",", "")))
    global_counters[x] = counters_formatted

champions_formatted.sort()
rows = list()
for champ in champions_formatted:
    row = list()
    row.append(champ)
    counters = global_counters[champ]
    for opponent in champions_formatted:
        stat = counters.get(opponent)
        row.append((stat[0] if stat is not None else None))
    rows.append(row)

headers = ["SELF"]
headers = headers + champions_formatted

print(rows)

with open("matchups_top_all.csv", "w", newline='') as f: 
    write = csv.writer(f) 
    write.writerow(headers)
    write.writerows(rows) 