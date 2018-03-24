from django.shortcuts import render

from typers.cashes.cash_layer import cached_round_ranking, cached_tournament_ranking, cached_matches_charts, \
    cached_open_tournaments


def index(request):
    context = cached_round_ranking()
    context.update(cached_tournament_ranking())
    context.update(cached_matches_charts())
    context.update(cached_open_tournaments(request.user))
    context.update({"form": ""})
    return render(request, 'index.html', context)
