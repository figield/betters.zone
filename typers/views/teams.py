from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from typers.cashes.cash_layer import cached_teams_menu, refresh_cached_teams_menu
from typers.forms.forms import TeamForm
from typers.models import Team, Photo


@csrf_protect
@login_required
def teams(request):
    context = dict()
    result = ""
    draft_name = ""
    created = False
    if request.method == 'POST':
        draft_name = request.POST.get('name')
        form = TeamForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            draft_name = ""
            name = form.cleaned_data.get('name')
            if Team.objects.filter(name=name, user=request.user).exists():
                result = "Your already have team with such name"
                context['created'] = False
            else:
                photo_raw = form.cleaned_data.get('photo')
                photo = None
                if photo_raw:
                    photo, _ = Photo.objects.get_or_create(file=photo_raw,
                                                           user=request.user,
                                                           title=name)
                team_obj, _ = Team.objects.get_or_create(name=name,
                                                         user=request.user,
                                                         defaults={'photo': photo})
                created = True
                result = "Successfully added a new team"
    else:
        form = TeamForm()

    if created:
        context['league_teams'] = refresh_cached_teams_menu(request.user)
    else:
        context['league_teams'] = cached_teams_menu(request.user)
    context['created'] = created
    context['draft_name'] = draft_name
    context['form'] = form
    context['result'] = result
    return render(request, 'typers/teams/create_team.html', context)
