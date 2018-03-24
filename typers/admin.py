from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from typers.models import Match, Round, Team, Prediction, TyperCard, Tournament, \
    Membership, Photo, League, Prize, Profile, Friendship, Notification, RoundRanking, TournamentRanking, \
    MatchStatistics

# def make_active(modeladmin, news, queryset):
#     queryset.update(is_active=True)
# make_active.short_description = u"Activate Users"
#
#
# def make_inactive(modeladmin, news, queryset):
#     queryset.update(is_active=False)
# make_inactive.short_description = u"Deactivate Users"


UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
# UserAdmin.actions.extend([make_active, make_inactive])

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(TournamentRanking)
class TournamentRankingAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'tournament_owner', 'advertise', 'statistics')

    @staticmethod
    def tournament_owner(obj):
        return obj.tournament.user.username


@admin.register(RoundRanking)
class RoundRankingAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'round', 'tournament_owner', 'advertise', 'statistics')

    @staticmethod
    def tournament_owner(obj):
        return obj.tournament.user.username


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_organizer', 'is_quiz_organizer', 'is_sponsor', 'birth_date', 'created_at', 'modified_at')


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'accepted', 'created_at', 'modified_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_sender', 'user_receiver', 'message', 'friendship', 'membership', 'created_at')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'tournament', 'tournament_owner', 'accepted', 'created_at', 'modified_at')

    @staticmethod
    def tournament_owner(obj):
        return obj.tournament.user.username


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user', 'order_number', 'template', 'tournament_link', 'active', 'open', 'rounds_num', 'created_at',
        'modified_at')


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'user', 'order_number', 'matches_num', 'created_at', 'modified_at')

    @staticmethod
    def user(obj):
        return obj.tournament.user.username

    @staticmethod
    def tournament(obj):
        return obj.tournament


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'order_number', 'tournament', 'round', 'sponsor',
        #'winner',
        'created_at', 'modified_at')


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template', 'created_at', 'modified_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'league', 'image_tag', 'created_at', 'modified_at')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<a href="/media/{}"><img width="50px" height="50px" src="/media/{}" /></a>' \
                               .format(obj.photo.file, obj.photo.file))
        else:
            return "No logo"

    image_tag.short_description = 'Image'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'image_tag', 'created_at', 'modified_at')

    def image_tag(self, obj):
        return format_html('<a href="/media/{}"><img width="50px" height="50px" src="/media/{}" /></a>' \
                           .format(obj.file, obj.file))

    image_tag.short_description = 'Image'


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'round', 'user', 'start_date', 'result1', 'result2', 'advertise', 'created_at', 'modified_at')

    @staticmethod
    def name(obj):
        return obj.team1.name + " vs " + obj.team2.name

    @staticmethod
    def user(obj):
        return obj.round.tournament.user.username


@admin.register(MatchStatistics)
class MatchStatisticsAdmin(admin.ModelAdmin):
    list_display = ('match', 'tournament', 'created_at', 'modified_at')


@admin.register(TyperCard)
class TyperCardAdmin(admin.ModelAdmin):
    list_display = (
        'round', 'tournament', 'user', 'tournament_link', 'points', 'has_real_predictions', 'predictions_num',
        'modified_at')


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('match', 'typer_card', 'result1', 'result2', 'points',
                    'correct1', 'correct2', 'correct_type', 'correct_result', 'created_at', 'modified_at')
