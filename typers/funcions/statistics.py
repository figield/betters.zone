from typers.models import MatchStatistics


def update_matchstatistics(match, tournament, p1_old, p2_old, p1_new, p2_new):
    if tournament is not None:
        match_statistics, _ = MatchStatistics.objects.get_or_create(match=match, tournament=tournament)
        new_stats, statistics = calculate_new_statistics(match_statistics.statistics,
                                                         p1_old, p2_old, p1_new, p2_new)
        if new_stats:
            match_statistics.statistics = statistics
            match_statistics.save()


def calculate_new_statistics(statistics, p1_old, p2_old, p1_new, p2_new):
    new_stats = False
    # Edge case: no statistics at all
    if not statistics:
        new_key = "%d:%d" % (p1_new, p2_new)
        statistics = {new_key: 1}
        new_stats = True
    elif p1_old != p1_new or p2_old != p2_new:
        # Decrease old prediction counter
        if p1_old is not None and p2_old is not None:
            old_key = "%d:%d" % (p1_old, p2_old)
            old_val = statistics.get(old_key)
            if old_val:
                statistics[old_key] = statistics.get(old_key) - 1
                if statistics[old_key] == 0:
                    statistics.pop(old_key)

        # Increase new prediction counter
        new_key = "%d:%d" % (p1_new, p2_new)
        statistics[new_key] = statistics.get(new_key, 0) + 1
        new_stats = True
    return new_stats, statistics
