from csv_utils import read_csv_all_champions_data


def get_best_counters():
    champions = read_csv_all_champions_data("top")

    pickates = [(x, champions[x]["pickrate"]) for x in champions]
    pickates.sort(key=lambda x: x[1], reverse=True)
    most_picks = pickates[:15]

    best_counters = list()
    for x in most_picks:
        counters = champions[x[0]]["counters"]
        counters_winrate = [(x.replace(".", "").replace(" ", "").replace("'", "").lower(), float(counters[x][0].replace("%", ""))) for x in counters]
        counters_winrate.sort(key=lambda x: x[1], reverse=False)
        negative_winrate = [x for x in counters_winrate if x[1] < 50]
        most_counters_champions = [x[0] for x in negative_winrate]
        best_counters += most_counters_champions

    best_counters_set = set(best_counters)
    counters_occurences = [(x, best_counters.count(x)) for x in best_counters_set]
    counters_occurences.sort(key=lambda x: x[1], reverse=True)
    print(counters_occurences)