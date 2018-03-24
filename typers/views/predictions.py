from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from typers.cashes.cash_layer import refresh_cached_tournaments_for_play
from typers.contexts.match import matches_for_charts_view
from typers.views.rankings import get_play_context
from typers.funcions.points import prediction_row
from typers.funcions.predictions import validate_prediction, update_prediction, check_if_updated_needed
from typers.funcions.statistics import update_matchstatistics
from typers.funcions.tournaments import get_tournament_and_round
from typers.models import TyperCard, Prediction, Friendship, Membership, Tournament


@login_required
def play(request):
    return render(request,
                  'typers/rankings/base_predictions.html',
                  get_play_context(request.user))


@csrf_protect
@login_required
def join_open_tournament(request, id_t):
    try:
        tournament = Tournament.objects.get(id=id_t, open=True)
    except ObjectDoesNotExist:
        return redirect('play')

    context = get_play_context(request.user)
    if request.user != tournament.user and request.user not in tournament.members.all():
        context['tournament_id'] = id_t
        context['tournament_name'] = tournament.name
        return render(request,
                      'typers/rankings/join_open_tournament.html',
                      context)
    else:
        context['already_joined'] = True
        return render(request,
                      'typers/rankings/base_predictions.html',
                      context)


@login_required
def tournament_accept_terms(request, id_t):
    try:
        tournament = Tournament.objects.get(id=id_t, open=True)
    except ObjectDoesNotExist:
        return redirect('play')

    accept = False
    if request.method == 'POST':
        accept = request.POST.get('termsaccept') == 'accept'

    if accept and request.user != tournament.user:
        # create new friendship
        friendship = Friendship.objects.filter(
            Q(user1=request.user, user2=tournament.user) | Q(user1=tournament.user, user2=request.user))
        if not friendship:
            sorted_users = sorted((request.user, tournament.user), key=lambda x: x.id)
            Friendship.objects.create(user1=sorted_users[0], user2=sorted_users[1],
                                      accepted=True, sender=tournament.user)

        # create new membership
        membership, _ = Membership.objects.get_or_create(user=request.user, tournament=tournament)
        membership.accepted = True
        membership.save()
        refresh_cached_tournaments_for_play(request.user)
    return redirect('play')


@csrf_protect
@login_required
def predictions_id(request, id_t, id_r):
    try:
        predictions_list, cloned_tournament, round_obj, show_save_button, any_points = make_predictions(request, id_t, id_r)
    except ObjectDoesNotExist:
        return redirect('play')

    context = get_play_context(request.user)
    context.update(predictions_table_context(predictions_list, cloned_tournament, round_obj, show_save_button, any_points))

    return render(request,
                  'typers/rankings/predictions.html',
                  context)


@csrf_protect
@login_required
def predictions_and_stats(request, id_t, id_r):
    try:
        predictions_list, cloned_tournament, round_obj, show_save_button, any_points = make_predictions(request, id_t, id_r)
    except ObjectDoesNotExist:
        return redirect('play')

    context = predictions_table_context(predictions_list, cloned_tournament, round_obj, show_save_button, any_points)

    tournament = round_obj.tournament
    matches = round_obj.match_set.all()
    global_matches_charts = []

    if cloned_tournament.id == tournament.id:
        # main tournament
        local_matches_charts = matches_for_charts_view(matches, tournament)
    else:
        local_matches_charts = matches_for_charts_view(matches, cloned_tournament)
        global_matches_charts = matches_for_charts_view(matches, tournament)

    context['matches_charts'] = True
    context['global_matches_charts'] = global_matches_charts
    context['local_matches_charts'] = local_matches_charts

    return render(request,
                  'typers/rankings/predictions_and_stats.html',
                  context)


def predictions_table_context(predictions_list, tournament, round_obj, show_save_button, any_points):
    context = dict()
    round_dict = dict()
    round_dict['name'] = round_obj.name
    round_dict['tournament'] = tournament.name
    context['predictions'] = sorted(predictions_list, key=lambda x: x['start_date'])
    context['round'] = round_dict
    context['show_save_button'] = show_save_button
    context['any_points'] = any_points
    return context


def make_predictions(request, id_t, id_r):
    tournament_obj, round_obj = get_tournament_and_round(request, id_t, id_r)
    if not tournament_obj or not round_obj:
        return False

    predictions_list = list()
    show_save_button = False
    any_points = False

    if round_obj.matches_num > 0:
        # TODO: do not create typerCard if there is no such need
        if tournament_obj.tournament_link is None:
            typer_card, _new = TyperCard.objects.get_or_create(user=request.user,
                                                               round=round_obj,
                                                               tournament=tournament_obj)
        else:
            typer_card, _new = TyperCard.objects.get_or_create(user=request.user,
                                                               round=round_obj,
                                                               tournament=tournament_obj,
                                                               tournament_link=tournament_obj.tournament_link)

        if request.method == 'POST':
            typer_card_updated = False
            for p in typer_card.prediction_set.all().select_related('match__team1').select_related('match__team2'):
                predictions_dict = dict()

                if timezone.now() > p.match.start_date:
                    predictions_dict['disabled'] = True
                    if p.match.result1 is not None and p.match.result1 > -1 and \
                                    p.match.result2 is not None and p.match.result2 > -1:
                        predictions_dict['info'] = p.points
                        any_points = True
                    else:
                        predictions_dict['info'] = "Waiting for update"
                else:
                    predictions_dict['disabled'] = False
                    show_save_button = True
                    predictions_dict['info'] = "Open"

                    prediction1 = request.POST.get('p1-' + str(p.match_id))
                    prediction2 = request.POST.get('p2-' + str(p.match_id))
                    if validate_prediction(prediction1) and validate_prediction(prediction2):
                        new_prediction1 = int(prediction1)
                        new_prediction2 = int(prediction2)
                        old_prediction1 = p.result1
                        old_prediction2 = p.result2
                        update_needed = check_if_updated_needed(new_prediction1, new_prediction2,
                                                                old_prediction1, old_prediction2)
                        if update_needed:
                            update_prediction(new_prediction1, new_prediction2, p)
                            update_matchstatistics(p.match, tournament_obj,
                                                   old_prediction1, old_prediction2,
                                                   new_prediction1, new_prediction2)
                            update_matchstatistics(p.match, tournament_obj.tournament_link,
                                                   old_prediction1, old_prediction2,
                                                   new_prediction1, new_prediction2)

                        typer_card_updated = typer_card_updated or update_needed

                predictions_list.append(prediction_row(predictions_dict, p, p.match))

            if typer_card_updated:
                # TODO: now predictionCard no need to have this attribute
                typer_card.has_real_predictions = typer_card_updated
                typer_card.save()

        else:  # GET
            for m in round_obj.match_set.all():
                predictions_dict = dict()
                p, _c = Prediction.objects.get_or_create(match=m, typer_card=typer_card)
                # TODO: do not create prediction if there is no need
                if timezone.now() > m.start_date:
                    predictions_dict['disabled'] = True
                    if m.result1 is not None and m.result1 > -1 and m.result2 is not None and m.result2 > -1:
                        predictions_dict['info'] = p.points
                        any_points = True
                    else:
                        predictions_dict['info'] = "Waiting for update"
                else:
                    predictions_dict['disabled'] = False
                    show_save_button = True
                    predictions_dict['info'] = "Open"

                predictions_list.append(prediction_row(predictions_dict, p, m))

    return predictions_list, tournament_obj, round_obj, show_save_button, any_points
