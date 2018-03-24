from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from project import settings
from typers.cashes.cash_layer import cached_tournaments_menu, cached_addmatch_context, refresh_cached_tournaments_menu, \
    refresh_cached_tournaments_for_play, cached_tournament_templates
from typers.forms.forms import MatchForm
from typers.funcions import tournaments
from typers.funcions.matches import save_matches
from typers.contexts.match import matches_for_table_view, matches_for_index_charts_view, matches_for_charts_view
from typers.models import Round, Match, Tournament


@csrf_protect
@login_required
def addmatch(request, round_id):
    try:
        cash_context = cached_addmatch_context(request.user, round_id)
    except (IndexError, AttributeError):
        # TODO: log sth
        return redirect('tournaments')

    context = dict()
    get_cashed = True
    if request.method == 'POST':
        form = MatchForm(request.POST)
        form.fields['team1'].choices = cash_context.get('teams_choices')
        form.fields['team2'].choices = cash_context.get('teams_choices')
        if form.is_valid():
            round_obj = cash_context.get('round_obj')
            if not tournaments.show_add_round(request.user, round_obj.matches_num):
                form.add_error('team1', "You cannot have more that " + settings.MAX_MATCHES + " matches in one round")
            else:
                team1_id = form.cleaned_data.get('team1')
                team2_id = form.cleaned_data.get('team2')
                if team1_id == team2_id:
                    form.add_error('team1', "Teams must differ")
                elif team1_id == '0':
                    form.add_error('team1', "Select team 1")
                elif team2_id == '0':
                    form.add_error('team2', "Select team 2")
                else:
                    start_date = form.cleaned_data.get('start_date')
                    start_time = form.cleaned_data.get('start_time')
                    dt = datetime.combine(start_date, start_time)
                    # if dt < timezone.now() - timedelta(minutes=60):
                    match_obj, created = Match.objects.get_or_create(
                        round_id=round_id,
                        team1_id=team1_id,
                        team2_id=team2_id,
                        start_date=dt,
                        defaults={'info': form.cleaned_data.get('info')})
                    if not created:
                        form.add_error('team1', "You already have such match")
                    else:
                        get_cashed = False
    else:
        form = MatchForm()
        form.fields['team1'].choices = cash_context.get('teams_choices')
        form.fields['team2'].choices = cash_context.get('teams_choices')

    if get_cashed:
        context['tournaments'] = cached_tournaments_menu(request.user)
    else:
        context['tournaments'] = refresh_cached_tournaments_menu(request.user)
        refresh_cached_tournaments_for_play(request.user)

    context['form'] = form
    context['teams'] = cash_context.get('teams')
    context['round'] = cash_context.get('round_dict')
    context['tournaments_choices'] = cached_tournament_templates()
    context['matches_charts'] = False
    context['matches'] = matches_for_table_view(cash_context['round_obj'].match_set.all())

    return render(request,
                  'typers/tournaments/match_create.html',
                  context)


@csrf_protect
@login_required
def results(request, round_id):
    round_dict = dict()
    try:
        round_obj = Round.objects.filter(id=round_id,
                                         tournament__user=request.user).select_related('tournament').prefetch_related(
            'match_set')[0]
        tournament = round_obj.tournament
        matches = round_obj.match_set.all()
        round_dict['name'] = round_obj.name
        round_dict['tournament'] = tournament.name
        round_dict['id'] = round_id
    except (IndexError, AttributeError):
        return redirect('tournaments')

    context = {'round': round_dict,
               'matches': matches_for_table_view(matches),
               'matches_charts': True,
               'global_matches_charts': matches_for_charts_view(matches, tournament),
               'local_matches_charts': [],
               'tournaments': cached_tournaments_menu(request.user),
               'tournaments_choices': cached_tournament_templates()}

    return render(request,
                  'typers/tournaments/matches_results.html',
                  context)


@login_required
def clonedresults(request, tournament_id, round_id):
    round_dict = dict()
    try:
        round_obj = Round.objects.filter(id=round_id,
                                         tournament__template=True).select_related('tournament').prefetch_related(
            'match_set')[0]
        cloned_tournament = Tournament.objects.filter(id=tournament_id)[0]
        tournament = round_obj.tournament
        matches = round_obj.match_set.all()
        round_dict['name'] = round_obj.name
        round_dict['tournament'] = tournament.name
        round_dict['id'] = round_id
    except (IndexError, AttributeError):
        return redirect('tournaments')

    context = {'round': round_dict,
               'matches': matches_for_table_view(matches),
               'matches_charts': True,
               'global_matches_charts': matches_for_charts_view(matches, tournament),
               'local_matches_charts': matches_for_charts_view(matches, cloned_tournament),
               'tournaments': cached_tournaments_menu(request.user),
               'tournaments_choices': cached_tournament_templates()}

    return render(request,
                  'typers/tournaments/cloned_matches_results.html',
                  context)


@csrf_protect
@login_required
def save_matches_results(request, round_id):
    save_matches(request, round_id)
    refresh_cached_tournaments_for_play(request.user)
    return redirect('results', round_id=round_id)
