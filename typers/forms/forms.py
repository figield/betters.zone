from django import forms
from django.utils import timezone

from typers.forms.fields import RestrictedImageField


class AddFriendForm(forms.Form):
    username = forms.CharField(
        label="Friend's username or email",
        max_length=255,
        required=True)


class PrizeForm(forms.Form):
    name = forms.CharField(
        label="Prize",
        max_length=255,
        required=True)
    order_number = forms.IntegerField(
        max_value=100,
        min_value=1)
    sponsor = forms.CharField(
        label="Prize sponsor",
        max_length=128,
        required=False)
    info = forms.CharField(
        required=False,
        label='Additional information',
        widget=forms.Textarea(
            attrs={'placeholder': 'Short prize description and terms'}))


class TeamForm(forms.Form):
    name = forms.CharField(
        label='Team/player name',
        max_length=255,
        required=True)
    photo = RestrictedImageField(
        required=False,
        label='Select the image',
        help_text='max. 42 KB')


class MatchForm(forms.Form):
    team1 = forms.ChoiceField(
        label='Team 1',
        required=True)
    team2 = forms.ChoiceField(
        label='Team 2',
        required=True)
    start_date = forms.DateField(
        widget=forms.SelectDateWidget,
        initial=timezone.now(),
        label='Start date',
        required=True)
    start_time = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M'),
        label='Start time (HH:MM)',
        initial=timezone.now(),
        required=True)
    info = forms.CharField(
        required=False,
        label='Additional information',
        max_length=255,
        widget=forms.Textarea(
            attrs={'placeholder': 'You can enter an extra information about this match'}))


class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(required=True)
