from django.core.cache import cache

from project.base_settings import USER_CACHE_TIMEOUT, INDEX_CACHE_TIMEOUT, SHORT_INDEX_CACHE_TIMEOUT
from typers.contexts.ranking import get_advertised_round_ranking_context, get_advertised_tournament_ranking_context
from typers.contexts.tournament import get_open_tournaments_context, get_tournaments_menu, get_tournament_templates
from typers.contexts.play import get_tournaments_for_play
from typers.contexts.team import get_teams_menu
from typers.contexts.match import get_addmatch_context, get_matches_charts_context


def cached_tournaments_menu(user):
    key = '%s_tournaments_tree' % user.username
    tournaments = cache.get(key, [])
    if not tournaments:
        tournaments = refresh_cached_tournaments_menu(user)
    return tournaments


def refresh_cached_tournaments_menu(user):
    key = '%s_tournaments_tree' % user.username
    tournaments = get_tournaments_menu(user)
    cache.set(key, tournaments, USER_CACHE_TIMEOUT)
    return tournaments


def cached_teams_menu(user):
    key = '%s_teams_tree' % user.username
    teams = cache.get(key, [])
    if not teams:
        teams = refresh_cached_teams_menu(user)
    return teams


def refresh_cached_teams_menu(user):
    key = '%s_teams_tree' % user.username
    teams = get_teams_menu(user)
    cache.set(key, teams, USER_CACHE_TIMEOUT)
    return teams


def cached_tournaments_for_play(user):
    key = '%s_predictions_tree' % user.username
    tournaments = cache.get(key, [])
    if not tournaments:
        tournaments = refresh_cached_tournaments_for_play(user)
    return tournaments


def refresh_cached_tournaments_for_play(user):
    key = '%s_predictions_tree' % user.username
    tournaments = get_tournaments_for_play(user)
    cache.set(key, tournaments, USER_CACHE_TIMEOUT)
    return tournaments


def cached_round_ranking():
    round_ranking = cache.get('round_ranking_context', {})
    if not round_ranking:
        round_ranking = get_advertised_round_ranking_context()
        cache.set('round_ranking_context', round_ranking, INDEX_CACHE_TIMEOUT)
    return round_ranking


def cached_tournament_ranking():
    tournament_ranking = cache.get('tournament_ranking_context', {})
    if not tournament_ranking:
        tournament_ranking = get_advertised_tournament_ranking_context()
        cache.set('tournament_ranking_context', tournament_ranking, INDEX_CACHE_TIMEOUT)
    return tournament_ranking


def cached_matches_charts():
    matches_charts = cache.get('matches_charts_context', {})
    if not matches_charts:
        matches_charts = get_matches_charts_context()
        cache.set('matches_charts_context', matches_charts, INDEX_CACHE_TIMEOUT)
    return matches_charts


def cached_open_tournaments(user):
    open_tournaments = cache.get('open_tournaments_context', {})
    if not open_tournaments:
        open_tournaments = get_open_tournaments_context(user)
        cache.set('open_tournaments_context', open_tournaments, SHORT_INDEX_CACHE_TIMEOUT)
    return open_tournaments


def cached_addmatch_context(user, round_id):
    key = '%s_addmatch_round_%s' % (user.username, round_id)
    addmatch_context = cache.get(key, {})
    if not addmatch_context:
        addmatch_context = get_addmatch_context(user, round_id)
        cache.set(key, addmatch_context, USER_CACHE_TIMEOUT)
    return addmatch_context


def cached_tournament_templates():
    tournament_templates = cache.get('tournament_templates_context', {})
    if not tournament_templates:
        tournament_templates = get_tournament_templates()
        cache.set('tournament_templates_context', tournament_templates, INDEX_CACHE_TIMEOUT)
    return tournament_templates
