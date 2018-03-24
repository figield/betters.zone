from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from project import settings
from typers.cashes.cash_layer import refresh_cached_tournaments_menu
from typers.funcions import tournaments
from typers.models import Tournament, Round


# AJAX
@csrf_protect
@login_required
def add_round(request, tournament_id):
    try:
        tournament_obj = Tournament.objects.get(id=tournament_id, user=request.user, tournament_link__isnull=True)
    except ObjectDoesNotExist:
        return redirect('tournaments')

    rounds_num = tournament_obj.rounds_num
    show_add_round = tournaments.show_add_round(request.user, rounds_num)
    context = dict()
    round_id = 0
    round_name = ""
    context['result'] = ""
    if show_add_round:
        if request.method == 'POST':
            round_name = str(rounds_num + 1)
            round_obj, created = Round.objects.get_or_create(name=round_name,
                                                             tournament=tournament_obj)
            if not created:
                context['result'] = 'You already have round with such name or number in this tournament'
            else:
                context['created'] = created
                if created:
                    refresh_cached_tournaments_menu(request.user)
                round_id = round_obj.id
                show_add_round = tournaments.show_add_round(request.user, rounds_num + 1)

    if not show_add_round:
        context['result'] = 'You cannot have more than ' + str(settings.MAX_ROUNDS) + ' rounds'

    context['show_add_round'] = show_add_round
    context['tournament_id'] = tournament_obj.id
    context['round_id'] = round_id
    context['round_name'] = round_name
    return JsonResponse(context)
