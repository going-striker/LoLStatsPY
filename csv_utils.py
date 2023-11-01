import csv
import random
import time
from get_champions import get_champions
from get_champions_counters import get_champion_counters

'''
GET LIST OF CHAMPIONS WITH RATES AND WRITE IN CSV
'''
def write_csv_champions(lane):
    champions = get_champions(lane)
    rows = list()
    for champ in champions:
        name = list()
        name.append(champ[0])
        name.append(champ[1])
        name.append(champ[2])
        name.append(champ[3])
        rows.append(name)
    with open("champions_{}.csv".format(lane), "w", newline='') as f: 
        write = csv.writer(f) 
        write.writerows(rows) 
    

'''
READ LIST OF CHAMPIONS WITH RATES FROM CSV
'''
def read_csv_champions(lane):
    file = open("champions_{}.csv".format(lane), "r")
    champions = list(csv.reader(file, delimiter=","))
    file.close()
    result = list()
    for champ in champions:
        result.append((champ[0], champ[1], champ[2], champ[3]))
    return result



'''
READ A CHAMPION MATCHUP / COUNTERS AND WRITE IN CSV
'''
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


'''
READ A CHAMPION MATCHUP / COUNTERS FROM CSV
'''
def read_csv_champion_counters(champion, lane):
    file = open("matchups/counters_{}_{}.csv".format(lane, champion), "r")
    counters = list(csv.reader(file, delimiter=","))
    file.close()
    result = dict()
    for champ in counters:
        result[champ[0]] = (champ[1], champ[2])
    return result


'''
READ CHAMPION RATES + MATCHUPS AND WRITE A CSV WITH GLOBAL MATCHUP INFO
'''
def write_csv_all_lane_matchups(lane):
    champions = read_csv_champions(lane)
    champions_formatted = [x[0].replace(".", "").replace(" ", "").replace("'", "").lower() for x in champions]
    global_counters = dict()
    for x in champions_formatted:
        counters = read_csv_champion_counters(x, lane)
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
    with open("matchups_top_all.csv", "w", newline='') as f: 
        write = csv.writer(f) 
        write.writerow(headers)
        write.writerows(rows) 


'''
REFRESH ALL DATA : GET CHAMPIONS / COUNTERS / GLOBAL MATCHUPS AND REWRITE ALL CSVs
'''
def refresh_data(lane):
    write_csv_champions(lane)   
    champions = read_csv_champions(lane)
    champions_formatted = [x[0].replace(".", "").replace(" ", "").replace("'", "").lower() for x in champions]
    for x in champions_formatted:
        write_csv_champion_counters(x, lane)
        time.sleep(2)
    write_csv_all_lane_matchups(lane)

def read_csv_all_champions_data(lane):
    result = dict()
    champions = read_csv_champions(lane)
    champions_formatted = [(x[0].replace(".", "").replace(" ", "").replace("'", "").lower(), float(x[1].replace("%", "")), float(x[2].replace("%", "")), float(x[3].replace("%", ""))) for x in champions]
    for x in champions_formatted:
        result[x[0]] = dict()
        result[x[0]]["winrate"] = x[1]
        result[x[0]]["pickrate"] = x[2]
        result[x[0]]["banrate"] = x[3]
        result[x[0]]["counters"] = read_csv_champion_counters(x[0], lane)
    return result

champions = read_csv_all_champions_data("top")
champions_name = [x for x in champions]
matchs = [random.choice(champions_name) for x in range(1000)]
print(matchs)

result = dict()
for x in champions_name:
    result[x] = 0
    counters = champions[x]["counters"]
    counters_formatter = { x.replace(".", "").replace(" ", "").replace("'", "").lower() : float(counters[x][0].replace("%", "")) for x in counters }
    for y in matchs:
        matchup = counters_formatter.get(y)
        if matchup is not None:
            result[x] += (matchup - 50)

result_list = [ (x, int(result[x])) for x in result ]
result_list.sort(key=lambda x: x[1], reverse=True)

rows = list()
for x in result_list:
    row = [ x[0], x[1] ]
    rows.append(row)

with open("1000_matchs_champions_score_top.csv", "w", newline='') as f: 
    write = csv.writer(f) 
    write.writerows(rows) 