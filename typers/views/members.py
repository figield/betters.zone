from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from typers.models import Tournament, Membership, Friendship, Notification, Profile
from typers.views.tournaments import get_tournament_context


@csrf_protect
@login_required
def add_friends_to_tournament(request, tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id, user=request.user)
    except ObjectDoesNotExist:
        return redirect('tournaments')

    accepted_members_of_tournament = list()
    pending_members_of_tournament = list()
    members_of_tournament = list()
    for ms in Membership.objects.filter(tournament=tournament).select_related('user'):
        members_of_tournament.append(ms.user)
        if ms.accepted:
            accepted_members_of_tournament.append({'username': ms.user.username})
        else:
            pending_members_of_tournament.append({'username': ms.user.username, 'membership_id': ms.id})

    friendships_not_in_tournament = list(Friendship.objects.filter(
        Q(user1=request.user, accepted=True) |
        Q(user2=request.user, accepted=True)).exclude(
        Q(user1__in=members_of_tournament) | Q(user2__in=members_of_tournament)))

    if request.method == 'POST':
        connected_friends_dict = dict()
        for friendship in friendships_not_in_tournament:
            connected_friends_dict[str(friendship.id)] = friendship

        for choice in request.POST.getlist('choices'):
            if choice in connected_friends_dict.keys():
                selected_friendship = connected_friends_dict.get(choice)
                friendships_not_in_tournament.remove(selected_friendship)
                if request.user == selected_friendship.user1:
                    membership_user = selected_friendship.user2
                else:
                    membership_user = selected_friendship.user1

                new_membership, cc = Membership.objects.get_or_create(user=membership_user,
                                                                      tournament=tournament)
                if cc:
                    message = "You have sent tournament (" + tournament.name + ") invitation to " + \
                              membership_user.username
                    Notification.objects.get_or_create(user_sender=request.user, user_receiver=request.user,
                                                       message=message, membership=new_membership)
                    message = "You have received tournament (" + tournament.name + ") invitation from " + \
                              request.user.username
                    Notification.objects.get_or_create(user_sender=request.user, user_receiver=membership_user,
                                                       message=message, membership=new_membership)
                    Profile.objects.filter(user=membership_user).update(has_notification=True)
                    pending_members_of_tournament.append({'username': membership_user.username,
                                                          'membership_id': new_membership.id})

    friendships_to_select = list()
    for friendship in friendships_not_in_tournament:
        if request.user == friendship.user1:
            friendship_user = friendship.user2
        else:
            friendship_user = friendship.user1
        friendships_to_select.append({'username': friendship_user.username,
                                      'friendship_id': friendship.id})

    context = dict()
    context['accepted_members_of_tournament'] = accepted_members_of_tournament
    context['friendships_to_select'] = friendships_to_select
    context['pending_members_of_tournament'] = pending_members_of_tournament
    return render(request,
                  'typers/tournaments/add_friends_to_tournament.html',
                  get_tournament_context(context, tournament, request.user))
