from django.utils import timezone

from typers.contexts.team import users_teams
from typers.models import Round, Match, MatchStatistics


def get_addmatch_context(user, round_id):
    teams = list(users_teams(user))
    teams_choices = sorted([(t.id, t.name) for t in teams], key=lambda x: x[1])
    round_obj = Round.objects.filter(id=round_id,
                                     tournament__user=user).select_related('tournament').first()
    round_dict = dict()
    round_dict['name'] = round_obj.name
    round_dict['tournament'] = round_obj.tournament.name
    round_dict['id'] = round_id
    addmatch_context = dict()
    addmatch_context['round_dict'] = round_dict
    addmatch_context['teams_choices'] = teams_choices
    addmatch_context['round_obj'] = round_obj
    addmatch_context['teams'] = teams
    return addmatch_context


def get_matches_charts_context():
    matches = Match.objects.filter(advertise=True)
    return {'matches_charts': matches_for_index_charts_view(matches)}


def matches_for_table_view(matches):
    matches_dict_list = list()
    for m in matches:
        md = dict()
        md["team1"] = m.team1.name
        md["team2"] = m.team2.name
        md["result1"] = m.result1
        md["result2"] = m.result2
        md["start_date"] = m.start_date
        md["id"] = m.id
        md["info"] = m.info
        warning = "Open"
        warning_info = ""
        if timezone.now() > m.start_date:
            warning = "Closed"
            if m.result1 is None or m.result2 is None or m.result1 == -1 or m.result2 == -1:
                warning_info += "Waiting for results"
        elif (m.result1 is not None) and (m.result2 is not None) and (m.result1 > -1) and (m.result2 > -1):
            warning_info += "How do you know the future results? Are you seer?"

        md["warning"] = warning
        md["warning_info"] = warning_info
        matches_dict_list.append(md)
    return sorted(matches_dict_list, key=lambda x: x['start_date'])


def matches_for_index_charts_view(matches):
    matches_dict_list = list()
    for m in matches:
        md = get_match_chart_data(m, m.round.tournament)
        if md:
            matches_dict_list.append(md)
    return matches_dict_list


def matches_for_charts_view(matches, tournament):
    matches_dict_list = list()
    for m in matches:
        md = get_match_chart_data(m, tournament)
        if md:
            matches_dict_list.append(md)
    return matches_dict_list


def get_match_chart_data(match, tournament):
    match_stats = MatchStatistics.objects.filter(match=match, tournament=tournament)
    md = dict()
    if match_stats:
        stats = match_stats[0].statistics
        md['match_name'] = match.team1.name + " vs " + match.team2.name
        md['id'] = str(match.id) + "_" + str(tournament.id)
        md['chartjs_data'] = [stats.get(k) for k in stats.keys()]
        md['chartjs_labels'] = [k for k in stats.keys()]
    return md
