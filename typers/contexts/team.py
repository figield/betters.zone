
def users_teams(user):
    return user.team_set.all() \
        .select_related('photo') \
        .select_related('league') \
        .order_by('-created_at')


def get_teams_menu(user):
    teams_by_league = dict()
    for team in users_teams(user):
        if team.league is not None:
            league_name = team.league.name
        else:
            league_name = 'default'
        teams_of_this_league = teams_by_league.get(league_name, [])
        teams_of_this_league.append(team)
        teams_by_league[league_name] = teams_of_this_league
    return list(teams_by_league.items())
