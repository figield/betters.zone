from django.core.management import BaseCommand
from django.utils import timezone
from typers.models import Team, Round, Match, Tournament
from django.contrib.auth.models import User


def get_admin_user():
    return User.objects.get(username="admin")


def load_teams(user):
    Team.objects.update_or_create(name="Legia Warszawa", user=user)
    Team.objects.update_or_create(name="Wisła Kraków", user=user)
    Team.objects.update_or_create(name="Team 3", user=user)
    Team.objects.update_or_create(name="Team 4", user=user)
    Team.objects.update_or_create(name="Team 5", user=user)
    Team.objects.update_or_create(name="Team 6", user=user)
    Team.objects.update_or_create(name="Team 7", user=user)
    Team.objects.update_or_create(name="Team 8", user=user)
    Team.objects.update_or_create(name="Team 9", user=user)
    Team.objects.update_or_create(name="Team 10", user=user)
    Team.objects.update_or_create(name="Team 11", user=user)
    Team.objects.update_or_create(name="Team 12", user=user)
    Team.objects.update_or_create(name="Team 13", user=user)
    Team.objects.update_or_create(name="Team 14", user=user)
    Team.objects.update_or_create(name="Team 15", user=user)
    Team.objects.update_or_create(name="Team 16", user=user)
    Team.objects.update_or_create(name="Team 17", user=user)
    Team.objects.update_or_create(name="Team 18", user=user)


def load_tournament(user):
    tournament, _c = Tournament.objects.update_or_create(name="Extra League 2017", user=user)
    return tournament


def load_rounds(tournament):
    Round.objects.update_or_create(name="Round 1 - 2017", tournament=tournament)


def load_matches():
    Match.objects.update_or_create(round_id=1, team1_id=1, team2_id=2, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=3, team2_id=4, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=5, team2_id=6, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=7, team2_id=8, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=9, team2_id=10, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=11, team2_id=12, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=13, team2_id=14, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=15, team2_id=16, start_date=timezone.now())
    Match.objects.update_or_create(round_id=1, team1_id=17, team2_id=18, start_date=timezone.now())


class Command(BaseCommand):
    help = 'Initialize database'

    def add_arguments(self, parser):
        parser.add_argument('--add-teams',
                            action='store_true',
                            dest='add-teams',
                            default=False,
                            help='Insert teams')
        parser.add_argument('--add-rounds',
                            action='store_true',
                            dest='add-rounds',
                            default=False,
                            help='Insert rounds')
        parser.add_argument('--add-matches',
                            action='store_true',
                            dest='add-matches',
                            default=False,
                            help='Insert matches')

    def handle(self, *args, **options):
        start = timezone.now()

        update_all = not any([options['add-teams'],
                              options['add-rounds'],
                              options['add-matches']])

        user = get_admin_user()
        tournament = load_tournament(user)

        if options['add-teams'] or update_all:
            print("Loading teams...")
            load_teams(user)

        if options['add-rounds'] or update_all:
            print("Loading round...")
            load_rounds(tournament)

        if options['add-matches'] or update_all:
            print("Loading matches...")
            load_matches()

        end = timezone.now()
        print(end - start)
