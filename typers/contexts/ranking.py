from typers.funcions.places import calculate_places
from typers.models import RoundRanking, TournamentRanking


def get_advertised_round_ranking_context():
    rankings = RoundRanking.objects.filter(advertise=True)
    if rankings:
        return get_round_ranking(rankings[0])
    else:
        return {'r_tournament_name': ""}


def get_advertised_tournament_ranking_context():
    rankings = TournamentRanking.objects.filter(advertise=True)
    if rankings:
        return get_tournament_ranking(rankings[0])
    else:
        return {'t_tournament_name': ""}


def get_tournament_ranking(ranking):
    context = dict()
    context['t_tournament_name'] = ranking.tournament.name
    context['t_results'] = calculate_places(ranking.statistics)
    return context


def get_round_ranking(ranking):
    context = dict()
    context['r_tournament_name'] = ranking.tournament.name
    context['r_round'] = ranking.round.name
    context['r_results'] = calculate_places(ranking.statistics)
    return context


def get_ranking_context(ranking):
    if ranking.statistics:
        return {'place': calculate_places(ranking.statistics)}
    else:
        return {'place': {}}
