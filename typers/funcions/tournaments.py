from project import settings
from typers.models import Tournament


def validate_tournament_name(tournament_name):
    return (tournament_name is not None) and (len(tournament_name.strip()) < 3)


def show_add_tournament(user, tour_num):
    return tour_num < settings.MAX_TOURNAMENTS or (user.is_staff and settings.IS_STAFF)


def show_add_round(user, rounds_num):
    return rounds_num < settings.MAX_ROUNDS or (user.is_staff and settings.IS_STAFF)


def show_add_match(user, matches_num):
    return matches_num < settings.MAX_MATCHES or (user.is_staff and settings.IS_STAFF)


def get_tournament_and_round(request, id_t, id_r):
    tournament_obj = friend_or_my_tournament(request, id_t)
    round_obj = None
    if tournament_obj:
        if tournament_obj.tournament_link is None:
            round_obj = tournament_obj.round_set.get(id=id_r)
        else:
            round_obj = tournament_obj.tournament_link.round_set.get(id=id_r)
    return tournament_obj, round_obj


def friend_or_my_tournament(request, id_t):
    tournament_obj = Tournament.objects.get(id=id_t, active=True)
    if tournament_obj.user.username == request.user.username:
        pass
    else:
        we_are_firends = Tournament.objects.filter(user=tournament_obj.user,
                                                   id=tournament_obj.id,
                                                   members=request.user,
                                                   tournament_membership__accepted=True).exists()
        if not we_are_firends:
            tournament_obj = None

    return tournament_obj
