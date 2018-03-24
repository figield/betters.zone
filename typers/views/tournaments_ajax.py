from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from project import settings
from typers.cashes.cash_layer import refresh_cached_tournaments_menu
from typers.funcions.tournaments import show_add_tournament, validate_tournament_name
from typers.models import Tournament


@csrf_protect
@login_required
def create_tournament(request):
    tour_num = request.user.tournament_set.count()
    show_add_tour = show_add_tournament(request.user, tour_num)
    context = dict()
    context['result'] = ""
    created = False
    if show_add_tour:
        if request.method == 'POST':
            tournament_name = request.POST.get('tournament_name')
            if validate_tournament_name(tournament_name):
                context['result'] = 'Tournament name is too short'
            else:
                tournament_name = tournament_name.strip()
                _tournament_obj, created = Tournament.objects.get_or_create(
                    name=tournament_name,
                    user=request.user)
                if not created:
                    context['result'] = 'You already have tournament with such name'
                else:
                    tour_num += 1
                    context['result'] = 'The tournament "' + tournament_name + '" was successfully created'
                    context['name'] = tournament_name
                    context['tournament_id'] = _tournament_obj.id
                    show_add_tour = show_add_tournament(request.user, tour_num)

    if not show_add_tour:
        context['result'] = 'You cannot have more than ' + str(settings.MAX_TOURNAMENTS) + ' tournaments'

    context['show_add_tournament'] = show_add_tour
    context['created'] = created
    if created:
        refresh_cached_tournaments_menu(request.user)
    return JsonResponse(context)


@csrf_protect
@login_required
def clone_tournament(request):
    context = dict()
    context['result'] = ""
    created = False
    tour_num = request.user.tournament_set.count()
    show_add_tour = show_add_tournament(request.user, tour_num)
    try:
        if show_add_tour:
            if request.method == 'POST':
                tournament_id = request.POST.get('tournament_id')
                selected_template_t = Tournament.objects.filter(id=tournament_id, template=True)[0]
                tournament_name = request.POST.get('tournament_name')
                if not tournament_name:
                    tournament_name = selected_template_t.name
                elif validate_tournament_name(tournament_name):
                    context['result'] = 'Tournament name is too short'
                    tournament_name = None
                else:
                    tournament_name = tournament_name.strip()

                if tournament_name:
                    _tournament_obj, created = Tournament.objects.get_or_create(
                        name=tournament_name,
                        user=request.user,
                        defaults={'tournament_link': selected_template_t})
                    if not created:
                        context['result'] = 'You already have tournament with such name'
                    else:
                        tour_num += 1
                        context['result'] = 'The tournament "' + selected_template_t.name + '" was successfully cloned'
                        context['name'] = tournament_name
                        context['tournament_id'] = _tournament_obj.id
                        rounds = list()
                        for r in selected_template_t.round_set.filter(matches_num__gt=0).order_by(
                                'created_at').reverse():
                            rounds.append({'name': r.name, 'id': r.id})
                        context['rounds'] = rounds
                        show_add_tour = show_add_tournament(request.user, tour_num)
    except (IndexError, AttributeError):
        pass

    if not show_add_tour:
        context['result'] = 'You cannot have more than ' + str(settings.MAX_TOURNAMENTS) + ' tournaments'

    context['show_add_tournament'] = show_add_tour
    context['created'] = created
    if created:
        refresh_cached_tournaments_menu(request.user)
    return JsonResponse(context)
