from typers.funcions.tournaments import show_add_round
from typers.models import Tournament


def get_open_tournaments_context(user):
    if user.is_anonymous():
        open_tournaments = Tournament.objects.filter(open=True, active=True) \
            .select_related('user')
    else:
        open_tournaments = Tournament.objects.filter(open=True, active=True) \
            .exclude(members=user) \
            .select_related('user')
    return {'open_tournaments': open_tournaments}


def get_tournaments_menu(user):
    tournaments = list()
    tournaments_obj = Tournament.objects.filter(user=user, active=True).prefetch_related(
        'round_set').order_by('-created_at')
    for t in tournaments_obj:
        tournament = dict()
        tournament['name'] = t.name
        tournament['id'] = t.id

        cloned = True
        if t.tournament_link is None:
            cloned = False
            t_rounds = t.round_set.all().order_by('created_at').reverse()
        else:
            t_rounds = t.tournament_link.round_set.filter(matches_num__gt=0).order_by('created_at').reverse()

        tournament['rounds'] = [{'name': r.name, 'id': r.id, 'num': r.matches_num} for r in t_rounds]
        tournament['cloned'] = cloned
        tournament['show_add_round'] = not cloned and show_add_round(user, t.rounds_num)

        tournaments.append(tournament)
    return tournaments


def get_tournament_templates():
    return sorted([(t.id, t.name) for t in Tournament.objects.filter(template=True)], key=lambda x: x[1])