import csv
import os
import shutil

from django.core.management import BaseCommand
from django.utils import timezone

from project.settings import BASE_DIR, MEDIA_ROOT
from typers.models import Team, Photo, League
from django.contrib.auth.models import User


def get_admin_user():
    return User.objects.get(username="admin")


def get_custom_user(custom_user):
    return User.objects.get(username=custom_user)


def get_teams_dict(league_name, resource_dir):
    teams_dict = dict()
    with open(os.path.join(resource_dir, league_name + '.csv')) as csvfile:
        for row_item in csv.reader(csvfile, delimiter=';'):
            teams_dict[row_item[0]] = row_item[1]
    return teams_dict


def copy_team_photo(user, league_name, resource_dir, teams):
    league_dir = os.path.join(MEDIA_ROOT, user.username + "/" + league_name)
    if not os.path.exists(league_dir):
        os.makedirs(league_dir)

    for team_name in teams.keys():
        photo_name = teams[team_name]
        print(photo_name)
        shutil.copy2(resource_dir + '/' + photo_name, league_dir)


def create_team_objects(user, league_name, teams):
    league_nice_name = " ".join(n[0].upper() + n[1:] for n in league_name.split("_"))
    league, _ = League.objects.get_or_create(name=league_nice_name,
                                             user=user,
                                             defaults={'template': True})

    for team_name in teams.keys():
        photo_name = teams[team_name]
        photo, created = Photo.objects.get_or_create(
            user=user,
            file=user.username + "/" + league_name + "/" + photo_name,
            title=team_name)

        Team.objects.update_or_create(name=team_name,
                                      user=user,
                                      defaults={'photo': photo,
                                                'league': league})


def load_teams(user, league_name):
    resource_dir = os.path.join(BASE_DIR, "resources/" + league_name)

    print("Read teams from resources")
    teams = get_teams_dict(league_name, resource_dir)

    print("Copy teams photos")
    copy_team_photo(user, league_name, resource_dir, teams)

    print("Creating team objects")
    create_team_objects(user, league_name, teams)


class Command(BaseCommand):
    help = 'Initialize database'

    def add_arguments(self, parser):
        parser.add_argument('--user',
                            type=str,
                            dest='user')

    def handle(self, *args, **options):
        start = timezone.now()

        custom_user = options['user']
        if custom_user:
            user = get_custom_user(custom_user)
        else:
            user = get_admin_user()

        load_teams(user, 'premier_league')
        load_teams(user, 'ekstraklasa')
        load_teams(user, 'bundesliga')
        load_teams(user, 'laLiga')
        load_teams(user, 'ligue 1')
        load_teams(user, 'serie_a')

        end = timezone.now()
        print(end - start)
