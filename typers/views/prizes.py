from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from typers.forms.forms import PrizeForm
from typers.models import Tournament, Prize, Round
from typers.views.tournaments import get_tournament_context


@csrf_protect
@login_required
def add_prize_for_tournament(request, tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id, user=request.user)
    except ObjectDoesNotExist:
        return redirect('tournaments')

    result = ""
    if request.method == 'POST':
        form = PrizeForm(request.POST)
        if form.is_valid():
            try:
                prize_obj, created = Prize.objects.get_or_create(
                    name=form.cleaned_data.get('name'),
                    order_number=form.cleaned_data.get('order_number'),
                    tournament=tournament,
                    round=None,
                    defaults={'sponsor': form.cleaned_data.get('sponsor'),
                              'info': form.cleaned_data.get('info')})
                if created:
                    result = "new_prize"
                    form = PrizeForm()
                else:
                    result = "already_exist"
            except MultipleObjectsReturned:
                result = "already_exist"
    else:
        form = PrizeForm()

    return render(request,
                  'typers/tournaments/prizes_for_tournament.html',
                  get_tournament_prize_context(None,
                                               tournament,
                                               form,
                                               result,
                                               request.user))


@csrf_protect
@login_required
def edit_prize_for_tournament(request, id_p):
    try:
        prize = Prize.objects.get(id=id_p, tournament__user=request.user)
        tournament = prize.tournament
    except ObjectDoesNotExist:
        return redirect('tournaments')

    result = ""
    if request.method == 'POST':
        form = PrizeForm(request.POST)
        if form.is_valid():
            prizes = Prize.objects.filter(
                name=form.cleaned_data.get('name'),
                order_number=form.cleaned_data.get('order_number'),
                tournament=tournament,
                round=None).count()
            if prizes == 0:
                prize.name = form.cleaned_data.get('name')
                prize.order_number = int(form.cleaned_data.get('order_number'))
                prize.sponsor = form.cleaned_data.get('sponsor')
                prize.info = form.cleaned_data.get('info')
                prize.save()
                result = "updated"
            else:
                result = "already_exist"
        else:
            result = "invalid_value"
    else:
        form = PrizeForm()

    return render(request,
                  'typers/tournaments/prizes_for_tournament.html',
                  get_tournament_prize_context(prize,
                                               tournament,
                                               form,
                                               result,
                                               request.user))


@csrf_protect
@login_required
def delete_prize_for_tournament(request, id_p):
    try:
        prize = Prize.objects.get(id=id_p, tournament__user=request.user)
        tournament = prize.tournament
    except ObjectDoesNotExist:
        return redirect('tournaments')

    prize.delete()
    return redirect('add_prize_for_tournament', tournament_id=tournament.id)


@csrf_protect
@login_required
def delete_prize_for_round(request, id_p):
    try:
        prize = Prize.objects.get(id=id_p, tournament__user=request.user)
        tournament = prize.tournament
        round_obj = prize.round
    except ObjectDoesNotExist:
        return redirect('tournaments')

    prize.delete()
    return redirect('add_prize_for_round', id_t=tournament.id, id_r=round_obj.id)


@csrf_protect
@login_required
def add_prize_for_round(request, id_t, id_r):
    try:
        tournament = Tournament.objects.get(id=id_t, user=request.user)
        if tournament.tournament_link is None:
            round_obj = Round.objects.get(id=id_r, tournament=tournament)
        else:
            round_obj = Round.objects.get(id=id_r, tournament=tournament.tournament_link)
    except ObjectDoesNotExist:
        return redirect('tournaments')

    result = ""
    if request.method == 'POST':
        form = PrizeForm(request.POST)
        if form.is_valid():
            try:
                _, created = Prize.objects.get_or_create(
                    name=form.cleaned_data.get('name'),
                    order_number=form.cleaned_data.get('order_number'),
                    tournament=tournament,
                    round=round_obj,
                    defaults={'sponsor': form.cleaned_data.get('sponsor'),
                              'info': form.cleaned_data.get('info')})
                if created:
                    result = "new_prize"
                    form = PrizeForm()
                else:
                    result = "already_exist"
            except MultipleObjectsReturned:
                result = "already_exist"
    else:
        form = PrizeForm()

    return render(request,
                  'typers/tournaments/prizes_for_round.html',
                  get_round_prize_context(None,
                                          round_obj,
                                          tournament,
                                          form,
                                          result,
                                          request.user))


@csrf_protect
@login_required
def edit_prize_for_round(request, id_p):
    try:
        prize = Prize.objects.get(id=id_p, tournament__user=request.user)
        tournament = prize.tournament
    except ObjectDoesNotExist:
        return redirect('tournaments')

    result = ""
    if request.method == 'POST':
        form = PrizeForm(request.POST)
        if form.is_valid():
            try:
                prize, created = Prize.objects.update_or_create(
                    id=prize.id,
                    defaults={'name': form.cleaned_data.get('name'),
                              'order_number': form.cleaned_data.get('order_number'),
                              'sponsor': form.cleaned_data.get('sponsor'),
                              'info': form.cleaned_data.get('info')})
                result = "updated"
            except IntegrityError:
                result = "already_exist"
        else:
            result = "invalid_value"
    else:
        form = PrizeForm()

    return render(request,
                  'typers/tournaments/prizes_for_round.html',
                  get_round_prize_context(prize,
                                          prize.round,
                                          tournament,
                                          form,
                                          result,
                                          request.user))


def get_prize_context(context, prize, tournament, form, result, user):
    context['prize'] = prize_to_context(prize)
    context['form'] = form
    context['result'] = result
    return get_tournament_context(context, tournament, user)


def get_round_prize_context(prize, round_obj, tournament, form, result, user):
    context = dict()
    context['round'] = round_obj.name
    context['round_id'] = round_obj.id
    context['prizes'] = Prize.objects.filter(tournament=tournament, round=round_obj).order_by('order_number')
    return get_prize_context(context, prize, tournament, form, result, user)


def get_tournament_prize_context(prize, tournament, form, result, user):
    context = dict()
    context['prizes'] = Prize.objects.filter(tournament=tournament, round__isnull=True).order_by('order_number')
    return get_prize_context(context, prize, tournament, form, result, user)


def prize_to_context(prize):
    context_prize = dict()
    if prize:
        context_prize['sponsor'] = prize.sponsor
        context_prize['info'] = prize.info
        context_prize['name'] = prize.name
        context_prize['order_number'] = prize.order_number
    else:
        context_prize['sponsor'] = ""
        context_prize['info'] = ""
        context_prize['name'] = ""
        context_prize['order_number'] = ""
    return context_prize
