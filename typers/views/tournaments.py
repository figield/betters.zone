from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from project import settings
from typers.cashes.cash_layer import cached_tournaments_menu, refresh_cached_tournaments_menu, \
    cached_tournament_templates
from typers.funcions.tournaments import show_add_tournament
from typers.models import Tournament


@csrf_protect
@login_required
def tournaments(request):
    return render(request,
                  'typers/tournaments/tournaments.html',
                  get_tournaments_context(dict(), request.user))


@login_required
def remove_tournament(request, tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id, user=request.user)
    except ObjectDoesNotExist:
        return redirect('tournaments')

    return render(request,
                  'typers/tournaments/remove_tournament.html',
                  get_tournament_context(dict(), tournament, request.user))


@login_required
def remove_tournament_accept(request, tournament_id):
    Tournament.objects.filter(id=tournament_id, user=request.user).delete()
    refresh_cached_tournaments_menu(request.user)
    return redirect('tournaments')


def get_tournament_context(context, tournament, user):
    context['tournament'] = tournament.name
    context['tournament_id'] = tournament.id
    context['cloned'] = tournament.tournament_link is not None
    return get_tournaments_context(context, user)


def get_tournaments_context(context, user):
    context['tournaments'] = cached_tournaments_menu(user)
    context['tournaments_choices'] = cached_tournament_templates()
    context['show_add_tournament'] = show_add_tournament(user, user.tournament_set.count())
    context['max_tournaments'] = settings.MAX_TOURNAMENTS
    context['matches_charts'] = False
    return context


