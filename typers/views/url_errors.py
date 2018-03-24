from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# TODO: log error

@login_required
def url_error_tournaments(request, sth=None):
    return redirect('tournaments')


@login_required
def url_error_friends(request, sth=None):
    return redirect('friends')


@login_required
def url_error_addfriendstotournament(request, sth=None):
    return redirect('addfriendstotournament')


@login_required
def url_error_predictions(request, sth=None):
    return redirect('play')
