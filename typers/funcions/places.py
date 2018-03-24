

def calculate_places(rankings):
    v = {}
    for key, value in rankings.items():
        v.setdefault(value, []).append(key)
    statistics = sorted(v.items(), key=lambda x: x[0], reverse=True)
    return calculate_place(1, dict(), statistics)


def calculate_place(place, result, statistics):
    if statistics:
        result[place] = dict()
        p, w = statistics.pop(0)
        result[place]['points'] = p
        result[place]['winners'] = ", ".join(w)
        next_place = place + len(w)
        return calculate_place(next_place, result, statistics)
    else:
        return result
