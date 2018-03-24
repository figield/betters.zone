from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from typers.cashes.cash_layer import cached_tournaments_for_play
from typers.contexts.ranking import get_ranking_context
from typers.funcions.tournaments import get_tournament_and_round, friend_or_my_tournament
from typers.models import RoundRanking, TournamentRanking


@login_required
def round_ranking(request, id_t, id_r):
    try:
        tournament_obj, round_obj = get_tournament_and_round(request, id_t, id_r)
    except ObjectDoesNotExist:
        return redirect('play')

    ranking, _ = RoundRanking.objects.get_or_create(tournament=tournament_obj,
                                                    round=round_obj)
    users_points = dict()
    if ranking.statistics:
        users_points = ranking.statistics

    round_dict = dict()
    round_dict['name'] = round_obj.name
    round_dict['tournament'] = tournament_obj.name
    context = get_play_context(request.user)
    context['ranking'] = sorted(users_points.items(), key=lambda x: x[1], reverse=True)
    context['podium'] = get_ranking_context(ranking)
    context['round'] = round_dict
    return render(request,
                  'typers/rankings/ranking_round_table.html',
                  context)


@login_required
def tournament_ranking(request, id_t):
    try:
        tournament_obj = friend_or_my_tournament(request, id_t)
    except ObjectDoesNotExist:
        return redirect('play')

    ranking, _ = TournamentRanking.objects.get_or_create(tournament=tournament_obj)

    users_points = dict()
    if ranking.statistics:
        users_points = ranking.statistics

    tournament_dict = dict()
    tournament_dict['name'] = tournament_obj.name
    context = get_play_context(request.user)
    context['ranking'] = sorted(users_points.items(), key=lambda x: x[1], reverse=True)
    context['podium'] = get_ranking_context(ranking)
    context['tournament'] = tournament_dict
    return render(request,
                  'typers/rankings/ranking_tournament_table.html',
                  context)


def get_play_context(user):
    return {'tournaments': cached_tournaments_for_play(user),
            'already_joined': False}
