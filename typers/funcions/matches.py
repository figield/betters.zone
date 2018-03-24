from datetime import datetime

from django.shortcuts import redirect

from typers.models import Round, TyperCard, RoundRanking, TournamentRanking


def save_matches(request, round_id):
    try:
        round_obj = Round.objects.filter(id=round_id, tournament__user=request.user). \
            select_related('tournament'). \
            prefetch_related('match_set')[0]
    except (IndexError, AttributeError):
        return redirect('tournaments')

    matches = round_obj.match_set.all().prefetch_related('prediction_set')
    changed = False
    for m in matches:
        result1 = request.POST.get('result1-' + str(m.id))
        result2 = request.POST.get('result2-' + str(m.id))
        if result1 and result1.isdigit() and result2 and result2.isdigit():
            if m.result1 != int(result1):
                m.result1 = int(result1)
                changed = True
            if m.result2 != int(result2):
                m.result2 = int(result2)
                changed = True
        elif not result1 and not result2:
            m.result1 = None
            m.result2 = None
            changed = True

        start_date = request.POST.get('start_date-' + str(m.id))
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%H:%M %d/%m/%Y')
                m.start_date = start_date
                changed = True
            except ValueError:
                pass

        info = request.POST.get('info-' + str(m.id))
        if info:
            m.info = info
            changed = True
        m.save()

    # check if all matches have changed and then recalculate rankings
    # Risk: Predictions might not be updated on time.
    # Also update cannot be done from the admin site.
    if changed:
        tournament_obj = round_obj.tournament
        update_round_ranking(round_obj, tournament_obj)
        update_linked_rounds_rankings(round_obj, tournament_obj)
        update_tournament_ranking(tournament_obj)
        update_linked_tournaments_rankings(tournament_obj)


def collect_user_typercard_points(users_points, user_typercard):
    username = user_typercard.user.username
    points = users_points.get(username)
    if not points:
        points = user_typercard.points
    else:
        points += user_typercard.points
    users_points[username] = points


def update_round_ranking(round_obj, tournament):
    users_points = dict()
    for typercard in TyperCard.objects.filter(tournament=tournament,
                                              round=round_obj,
                                              has_real_predictions=True).select_related('user'):
        collect_user_typercard_points(users_points, typercard)
    RoundRanking.objects.update_or_create(tournament=tournament,
                                          round=round_obj,
                                          defaults={'statistics': users_points})


def update_linked_rounds_rankings(round_obj, template_tournament):
    for child_tournament in template_tournament.linked_tournaments_set.filter(template=False):
        update_round_ranking(round_obj, child_tournament)


def update_tournament_ranking(tournament_obj):
    users_points = dict()
    for typercard_obj in TyperCard.objects.filter(tournament=tournament_obj,
                                                  has_real_predictions=True).select_related('user'):
        collect_user_typercard_points(users_points, typercard_obj)
    TournamentRanking.objects.update_or_create(tournament=tournament_obj,
                                               defaults={'statistics': users_points})


def update_linked_tournaments_rankings(template_tournament):
    for child_tournament in template_tournament.linked_tournaments_set.filter(template=False):
        update_tournament_ranking(child_tournament)
