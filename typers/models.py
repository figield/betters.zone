from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


# class Sport(models.Model):
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(User, related_name='sport_set')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         unique_together = ('name', 'user')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_organizer = models.BooleanField(default=False)
    is_quiz_organizer = models.BooleanField(default=True)
    is_sponsor = models.BooleanField(default=False)
    has_notification = models.BooleanField(default=False)
    # Defaults:
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return self.user.username + "(" + self.user.get_full_name() + ")"
        else:
            return self.user.username


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='user1_friendships')
    user2 = models.ForeignKey(User, related_name='user2_friendships')
    # Defaults:
    sender = models.ForeignKey(User, related_name='sender_friendships')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user1', 'user2')


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='tournament_set')
    # Defaults:
    order_number = models.PositiveSmallIntegerField(default=1)
    tournament_link = models.ForeignKey('Tournament', null=True, blank=True, related_name='linked_tournaments_set')
    template = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    open = models.BooleanField(default=False)
    members = models.ManyToManyField(User, through='Membership', related_name='member_tournaments')
    rounds_num = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'user')


class Membership(models.Model):
    user = models.ForeignKey(User, related_name='user_membership')
    tournament = models.ForeignKey(Tournament, related_name='tournament_membership')
    # Defaults:
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tournament')


class Notification(models.Model):
    user_sender = models.ForeignKey(User, related_name='user_sender_notifications')
    user_receiver = models.ForeignKey(User, related_name='user_receiver_notifications')
    # Defaults:
    message = models.CharField(max_length=1024)
    friendship = models.ForeignKey(Friendship, null=True, blank=True)
    membership = models.ForeignKey(Membership, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Round(models.Model):
    name = models.CharField(max_length=50)
    order_number = models.PositiveSmallIntegerField(default=1)
    tournament = models.ForeignKey(Tournament)
    # Defaults:
    matches_num = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tournament.name + " : " + self.name

    class Meta:
        unique_together = ('name', 'tournament')


class Prize(models.Model):
    name = models.CharField(max_length=255)
    order_number = models.PositiveSmallIntegerField(default=1)
    tournament = models.ForeignKey(Tournament)
    # Defaults:
    round = models.ForeignKey(Round, null=True, blank=True)
    sponsor = models.CharField(max_length=128, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'order_number', 'tournament', 'round')


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_name/<filename>
    return '{0}/{1}'.format(instance.user.username, filename)


class Photo(models.Model):
    user = models.ForeignKey(User)
    file = models.ImageField(upload_to=user_directory_path, verbose_name='Image')
    title = models.CharField(max_length=128)
    # Defaults:
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class League(models.Model):
    name = models.CharField(max_length=200, default="default")
    user = models.ForeignKey(User)
    # Defaults:
    template = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'user')


class Team(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    # Defaults:
    league = models.ForeignKey(League, blank=True, null=True)
    photo = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)
   # show_photo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # def get_photo(self): teraz można usunąć wszystkie zdjecia, templejty załaduja defultowy obrazek
    #     if self.show_photo:
    #         return self.photo
    #     else:
    #         return Photo.objects.get(title="default", user__username="admin")

    class Meta:
        unique_together = ('name', 'user')


class Match(models.Model):
    round = models.ForeignKey(Round)
    team1 = models.ForeignKey(Team, related_name='team1_set')
    team2 = models.ForeignKey(Team, related_name='team2_set')
    # Defaults:
    start_date = models.DateTimeField()
    result1 = models.SmallIntegerField(default=-1, blank=True, null=True)
    result2 = models.SmallIntegerField(default=-1, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    advertise = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team1.name + " vs " + self.team2.name

    class Meta:
        unique_together = ('round', 'team1', 'team2', 'start_date')


class MatchStatistics(models.Model):
    match = models.ForeignKey(Match)
    tournament = models.ForeignKey(Tournament)
    # Defaults:
    statistics = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "(" + self.tournament.user.username + ") " + self.match.__str__() + " in " + self.tournament.name

    class Meta:
        unique_together = ('match', 'tournament')


# class Event(models.Model):
#     name = models.CharField(max_length=255)
#     round = models.ForeignKey(Round)
#     # Defaults:
#     players = models.ManyToManyField(Team, related_name='players')
#     start_date = models.DateTimeField()
#     # result = ??
#     info = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         unique_together = ('name', 'round')


class TyperCard(models.Model):
    round = models.ForeignKey(Round)
    tournament = models.ForeignKey(Tournament, related_name='typercards_set')
    user = models.ForeignKey(User)
    # Defaults:
    tournament_link = models.ForeignKey('Tournament', null=True, blank=True, related_name='linked_typercards')
    points = models.IntegerField(default=0)
    predictions_num = models.PositiveSmallIntegerField(default=0)
    has_real_predictions = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.tournament_link:
            return self.tournament.name + " (cloned): " + self.round.name + ": " + self.user.username
        else:
            return self.tournament.name + ": " + self.round.name + ": " + self.user.username

    class Meta:
        unique_together = ('round', 'tournament', 'user')


class Prediction(models.Model):
    match = models.ForeignKey(Match)
    typer_card = models.ForeignKey(TyperCard)
    # Defaults:
    result1 = models.SmallIntegerField(null=True, blank=True)  # TODO: what if someone will put big int?
    result2 = models.SmallIntegerField(null=True, blank=True)
    points = models.SmallIntegerField(default=0)
    correct1 = models.BooleanField(default=False)
    correct2 = models.BooleanField(default=False)
    correct_type = models.BooleanField(default=False)
    correct_result = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.typer_card.user.get_username() + ' - ' \
               + self.match.round.name + ": " + self.match.team1.name + " vs " + self.match.team2.name + ' - ' \
               + str(self.result1) + " : " + str(self.result2)

    class Meta:
        unique_together = ('match', 'typer_card')


class RoundRanking(models.Model):
    tournament = models.ForeignKey(Tournament)
    round = models.ForeignKey(Round)
    # Defaults:
    advertise = models.BooleanField(default=False)
    statistics = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tournament', 'round')

    def __str__(self):
        return self.tournament.name + ", round: " + self.round.name


class TournamentRanking(models.Model):
    tournament = models.ForeignKey(Tournament)
    # Defaults:
    advertise = models.BooleanField(default=False)
    statistics = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tournament.name
