from django.db.models import Q
from django.utils import timezone

from typers.models import Tournament, RoundRanking, TournamentRanking


def get_tournaments_for_play(user):
    tournaments_obj = Tournament.objects.filter(Q(members=user,
                                                  tournament_membership__accepted=True,
                                                  active=True) |
                                                Q(user=user,
                                                  active=True)) \
        .select_related('user') \
        .prefetch_related('round_set') \
        .distinct()

    tournaments_list = list()
    for tour in tournaments_obj:
        tournament = dict()
        tournament['id'] = tour.id
        tournament['name'] = tour.name
        tournament['organizer'] = tour.user.username
        open_rounds = list()
        closed_rounds = list()
        if tour.tournament_link is None:
            t_rounds = tour.round_set.all().order_by('-modified_at')
        else:
            tournament['id_cloned'] = tour.tournament_link.id
            t_rounds = tour.tournament_link.round_set.all().order_by('-modified_at')

        for t_round in t_rounds:  # .values('name', 'id', 'matches_num'):
            t_round_dict = dict()
            t_round_dict['has_ranking'] = RoundRanking.objects.filter(tournament=tour, round=t_round).exists()
            t_round_dict['name'] = t_round.name
            t_round_dict['id'] = t_round.id
            t_round_dict['matches_num'] = t_round.matches_num

            if t_round.match_set.filter(start_date__gt=timezone.now()).exists():
                open_rounds.append(t_round_dict)
            else:
                closed_rounds.append(t_round_dict)

        tournament['closed_rounds'] = closed_rounds
        tournament['open_rounds'] = open_rounds
        tournament['has_tournament_ranking'] = TournamentRanking.objects.filter(tournament=tour).exists()
        tournaments_list.append(tournament)
    return tournaments_list
