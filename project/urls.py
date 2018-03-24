from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from project import settings
from django.conf.urls.static import static
from typers.views.friends import cancel_friendship_invitation, friends, \
    accept_tournament_invitation, cancel_friendship, accept_friendship_invitation, cancel_tournament_invitation, \
    reject_tournament_invitation, cancel_tournament_invitation_as_organizer
from typers.views.rankings import round_ranking, tournament_ranking
from typers.views.index import index
from typers.views.registration import RegistrationViewUniqueEmail, resend_activation_email
from typers.views.predictions import play, predictions_id, join_open_tournament, tournament_accept_terms, \
    predictions_and_stats
from typers.views.tournaments import tournaments, remove_tournament, remove_tournament_accept
from typers.views.prizes import add_prize_for_tournament, edit_prize_for_tournament, \
    delete_prize_for_tournament, delete_prize_for_round, add_prize_for_round, edit_prize_for_round
from typers.views.members import add_friends_to_tournament
from typers.views.tournaments_ajax import create_tournament, clone_tournament
from typers.views.teams import teams
from typers.views.matches import addmatch, results, clonedresults, save_matches_results
from typers.views.rounds import add_round

urlpatterns = [
                  url(r'^adminzone/', admin.site.urls),
                  url(r'^$', index, name='index'),
                  url(r'^logout/$', logout_then_login, name='site-logout'),

                  url(r'^accounts/register/$', RegistrationViewUniqueEmail.as_view(), name='registration_register'),
                  url(r'^accounts/resend_registration/$', resend_activation_email, name='resend_registration_email'),

                  url(r'^accounts/', include('registration.backends.hmac.urls')),

                  # url(r'^accounts/activate/complete/$', TemplateView.as_view(
                  #     template_name='registration/activation_complete.html'),
                  #     name='registration_activation_complete'),
                  # # The activation key can make use of any character from the
                  # # URL-safe base64 alphabet, plus the colon as a separator.
                  # # url(r'^accounts/activate/(?P<activation_key>[-:\w]+)/$', views.ActivationView.as_view(),
                  # #     name='registration_activate'),
                  # # url(r'^accounts/register/$', views.RegistrationView.as_view(),
                  # #     name='registration_register'),
                  # url(r'^accounts/register/complete/$', TemplateView.as_view(
                  #     template_name='registration/registration_complete.html'),
                  #     name='registration_complete'),
                  # url(r'^accounts/register/closed/$', TemplateView.as_view(
                  #     template_name='registration/registration_closed.html'),
                  #     name='registration_disallowed'),

                  #     url(r'', include('registration.auth_urls')) :
                  # url(r'^accounts/login/$', name='auth_login'),
                  # url(r'^accounts/logout/$', name='auth_logout'),
                  # url(r'^accounts/password/change/$', name='auth_password_change'),
                  # url(r'^accounts/password/change/done/$', name='auth_password_change_done'),
                  # url(r'^accounts/password/reset/$', name='auth_password_reset'),
                  # url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                  #     name='auth_password_reset_confirm'),
                  # url(r'^accounts/password/reset/complete/$', name='auth_password_reset_complete'),
                  # url(r'^accounts/password/reset/done/$', name='auth_password_reset_done'),

                  url(r'^play/?$', play, name='play'),
                  # url(r'^play/(?P<sth>.*)?/?$', url_error_predictions),

                  url(r'^prediction/(?P<id_t>\d+)/(?P<id_r>\d+)/?$', predictions_id, name='predictions-id'),
                  # url(r'^prediction/(?P<sth>.*)?/?$', url_error_predictions),

                  url(r'^predictionsandstats/(?P<id_t>\d+)/(?P<id_r>\d+)/?$', predictions_and_stats,
                      name='predictionsandstats'),

                  url(r'^roundranking/(?P<id_t>\d+)/(?P<id_r>\d+)/?$', round_ranking, name='roundranking-id'),
                  # url(r'^roundranking/(?P<sth>.*)?/?$', url_error_predictions),

                  url(r'^tournamentranking/(?P<id_t>\d+)/?$', tournament_ranking, name='tournamentranking-id'),
                  # url(r'^tournamentranking/(?P<sth>.*)?/?$', url_error_predictions),

                  url(r'^tournaments/?$', tournaments, name='tournaments'),
                  url(r'^tournaments/join/(?P<id_t>\d+)/?$', join_open_tournament, name='joinopentournament_id'),
                  url(r'^tournaments/join/(?P<id_t>\d+)/accept/?$', tournament_accept_terms,
                      name='tournamentacceptterms-id'),
                  # url(r'^tournaments/(?P<sth>.*)?/?$', url_error_tournaments),

                  url(r'^teams/?$', teams, name='teams'),

                  # AJAX
                  url(r'^create_tournament/?$', create_tournament, name='create_tournament'),
                  url(r'^clone_tournament/?$', clone_tournament, name='clone_tournament'),
                  url(r'^add_round/(?P<tournament_id>\d+)/?$', add_round, name='add_round'),
                  # url(r'^add_round/(?P<sth>.*)?/?$', url_error_tournaments),
                  # ----

                  url(r'^addmatch/(?P<round_id>\d+)/?$', addmatch, name='addmatch'),
                  # url(r'^addmatch/(?P<sth>.*)?/?$', url_error_tournaments),

                  url(r'^results/(?P<round_id>\d+)/?$', results, name='results'),
                  # url(r'^results/(?P<sth>.*)?/?$', url_error_tournaments),

                  url(r'^clonedresults/(?P<tournament_id>\d+)/(?P<round_id>\d+)/?$', clonedresults,
                      name='clonedresults'),
                  # url(r'^clonedresults/(?P<sth>.*)?/?$', url_error_tournaments),

                  url(r'^savematchesresults/(?P<round_id>\d+)/?$', save_matches_results, name='save_matches_results'),
                  # url(r'^savematchesresults/(?P<sth>.*)?/?$', url_error_tournaments),

                  url(r'^removetournament/(?P<tournament_id>\d+)/?$', remove_tournament, name='remove_tournament'),
                  # url(r'^removetournament/(?P<sth>.*)?/?$', url_error_addfriendstotournament),

                  url(r'^removetournamentaccept/(?P<tournament_id>\d+)/?$', remove_tournament_accept,
                      name='remove_tournament_accept'),  # ensure that you want to remove tournament
                  # url(r'^removetournamentaccept/(?P<sth>.*)?/?$', url_error_addfriendstotournament),

                  url(r'^addprizefortournament/(?P<tournament_id>\d+)/?$', add_prize_for_tournament,
                      name='add_prize_for_tournament'),
                  url(r'^editprizefortournament/(?P<id_p>\d+)/?$', edit_prize_for_tournament,
                      name='edit_prize_for_tournament'),
                  url(r'^deleteprizefortournament/(?P<id_p>\d+)/?$', delete_prize_for_tournament,
                      name='delete_prize_for_tournament'),

                  url(r'^addprizeforround/(?P<id_t>\d+)/(?P<id_r>\d+)/?$', add_prize_for_round,
                      name='add_prize_for_round'),
                  url(r'^editprizeforround/(?P<id_p>\d+)/?$', edit_prize_for_round, name='edit_prize_for_round'),
                  url(r'^deleteprizeforround/(?P<id_p>\d+)/?$', delete_prize_for_round, name='delete_prize_for_round'),

                  # TOURNAMENTS INVITATIONS
                  url(r'^addfriendstotournament/(?P<tournament_id>\d+)/?$', add_friends_to_tournament,
                      name='add_friends_to_tournament'),
                  # url(r'^addfriendstotournament/(?P<sth>.*)?/?$', url_error_addfriendstotournament),

                  url(r'^accepttournamanetinvitation/(?P<membership_id>\d+)/?$', accept_tournament_invitation,
                      name='accept_tournament_invitation'),
                  # url(r'^accepttournamanetinvitation/(?P<sth>.*)?/?$', url_error_friends),

                  url(r'^canceltournamentinvitation/(?P<membership_id>\d+)/?$', cancel_tournament_invitation,
                      name='cancel_tournament_invitation'),

                  url(r'^canceltournamentinvitationasorganizer/(?P<membership_id>\d+)/?$',
                      cancel_tournament_invitation_as_organizer, name='cancel_tournament_invitation_as_organizer'),
                  # url(r'^canceltournamentinvitation/(?P<sth>.*)?/?$', url_error_friends),

                  url(r'^rejecttournamentinvitation/(?P<membership_id>\d+)/?$', reject_tournament_invitation,
                      name='reject_tournament_invitation'),
                  # url(r'^rejecttournamentinvitation/(?P<sth>.*)?/?$', url_error_friends),

                  # FRIENDSHIPS
                  url(r'^friends/?$', friends, name='friends'),

                  url(r'^acceptfriendshipinvitation/(?P<friendship_id>\d+)/?$', accept_friendship_invitation,
                      name='accept_friendship_invitation'),
                  # url(r'^acceptfriendshipinvitation/(?P<sth>.*)?/?$', url_error_friends),

                  url(r'^cancelfriendshipinvitation/(?P<friendship_id>\d+)/?$', cancel_friendship_invitation,
                      name='cancel_friendship_invitation'),
                  # url(r'^cancelfriendshipinvitation/(?P<sth>.*)?/?$', url_error_friends),

                  url(r'^cancelfriendship/(?P<friendship_id>\d+)/?$', cancel_friendship, name='cancel_friendship'),
                  # url(r'^cancelfriendship/(?P<sth>.*)?/?$', url_error_friends),

                  url(r'^quiz/?', include('quiz.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # + \
# [
#     url(r'^(?!/?static/)(?P<path>.*\..*)$',
#         RedirectView.as_view(url='/static/%(path)s', permanent=False))
# ]

if settings.TOOLBAR:
    print("Import debug_toolbar")
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
