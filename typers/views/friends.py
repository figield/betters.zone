from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from typers.cashes.cash_layer import refresh_cached_tournaments_for_play
from typers.forms.forms import AddFriendForm
from typers.models import Membership, Friendship, Notification, Profile


def context_for_friends(user):
    Profile.objects.filter(user=user).update(has_notification=False)
    user_friends = []
    for friendship in Friendship.objects.filter(Q(user1=user, accepted=True) | Q(user2=user, accepted=True)):
        if user == friendship.user1:
            user_friends.append({'friend_username': friendship.user2.username,
                                 'friendship_id': friendship.id})
        else:
            user_friends.append({'friend_username': friendship.user1.username,
                                 'friendship_id': friendship.id})

    user_notifications = []
    for notification in Notification.objects.filter(user_receiver=user) \
            .select_related('friendship').select_related('membership'):
        if notification.friendship:
            user_notifications.append({
                'sender': notification.user_sender == user,
                'message': notification.message,
                'friendship_id': notification.friendship_id,
                'membership_id': False,
                'date': notification.created_at})
        elif notification.membership:
            user_notifications.append({
                'sender': notification.user_sender == user,
                'message': notification.message,
                'friendship_id': False,
                'membership_id': notification.membership_id,
                'date': notification.created_at})

    return {'user_friends': user_friends,
            'user_notifications': user_notifications}


@login_required
def accept_friendship_invitation(request, friendship_id):
    friendships = Friendship.objects.filter(
        Q(user1=request.user, id=friendship_id) |
        Q(user2=request.user, id=friendship_id))
    if friendships:
        friendship = friendships[0]
        friendship.accepted = True
        friendship.save()
        # delete notification for user1 and user2
        Notification.objects.filter(friendship=friendship).delete()
    return redirect('friends')


@login_required
def cancel_friendship_invitation(request, friendship_id):
    Friendship.objects.filter(
        Q(user1=request.user, id=friendship_id) |
        Q(user2=request.user, id=friendship_id)).delete()
    # related notifications will be removed automatically
    return redirect('friends')


@login_required
def cancel_friendship(request, friendship_id):
    friendships = Friendship.objects.filter(
        Q(user1=request.user, id=friendship_id) |
        Q(user2=request.user, id=friendship_id)).select_related('user1').select_related('user2')

    if friendships:
        friendship = friendships[0]
        friendship.delete()
        # remove not accepted tournaments invitations
        Membership.objects.filter(Q(user=friendship.user1, accepted=False) |
                                  Q(user=friendship.user2, accepted=False)).delete()

    return redirect('friends')


@csrf_protect
@login_required
def friends(request):
    user1 = request.user
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            found_users = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)) \
                .exclude(username=request.user.username) \
                .exclude(email=request.user.username)
            if found_users:
                user2 = found_users[0]
                sorted_users = sorted([user1, user2], key=lambda x: x.id)
                friendships = Friendship.objects.filter(user1=sorted_users[0],
                                                        user2=sorted_users[1])
                if friendships:
                    friendship = friendships[0]
                    if friendship.sender == user2:
                        # user2 already has sent the invitation, so this request will accept it
                        friendship.accepted = True
                        friendship.save()
                        # delete notification for user1 and user2
                        Notification.objects.filter(friendship=friendship).delete()
                    else:
                        form.add_error('username', "Invitation was already sent")
                else:
                    new_friendship = Friendship.objects.create(user1=sorted_users[0],
                                                               user2=sorted_users[1],
                                                               sender=user1)
                    # create notifications for user1 and user2:
                    message = "You have sent friendship invitation to " + user2.username
                    Notification.objects.get_or_create(user_sender=user1, user_receiver=user1,
                                                       message=message, friendship=new_friendship)
                    message = "You have received friendship invitation from " + user1.username
                    Profile.objects.filter(user=user2).update(has_notification=True)
                    Notification.objects.get_or_create(user_sender=user1, user_receiver=user2,
                                                       message=message, friendship=new_friendship)
            else:
                form.add_error('username', "There is no such user")
    else:
        form = AddFriendForm()

    context = context_for_friends(user1)
    context['form'] = form

    return render(request, 'typers/friends/base_friends.html', context)


@login_required
def accept_tournament_invitation(request, membership_id):
    memberships = Membership.objects.filter(id=membership_id, user=request.user)
    if memberships:
        membership = memberships[0]
        membership.accepted = True
        membership.save()
        # delete notifications for user1 and user2
        Notification.objects.filter(membership=membership).delete()
        refresh_cached_tournaments_for_play(request.user)
    return redirect('friends')


@login_required
def cancel_tournament_invitation(request, membership_id):
    memberships = Membership.objects.filter(id=membership_id).select_related('tournament')
    if memberships and memberships[0].tournament.user == request.user:
        membership = memberships[0]
        membership.delete()
        # related notifications will be removed automatically
    return redirect('friends')


@login_required
def cancel_tournament_invitation_as_organizer(request, membership_id):
    memberships = Membership.objects.filter(id=membership_id).select_related('tournament')
    tournament_id = 0
    if memberships and memberships[0].tournament.user == request.user:
        tournament_id = memberships[0].tournament_id
        memberships[0].delete()
        # related notifications will be removed automatically
    return redirect('add_friends_to_tournament', tournament_id=tournament_id)


@login_required
def reject_tournament_invitation(request, membership_id):
    memberships = Membership.objects.filter(id=membership_id, user=request.user)
    if memberships:
        memberships[0].delete()
        # related notifications will be removed automatically
    return redirect('friends')
