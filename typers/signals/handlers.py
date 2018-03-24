from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from typers.funcions.points import update_predictions_points
from typers.models import Match, Round, Prediction
from typers.models import Profile


# TODO: logs msg - reports, test with deugger and logs analysis


@receiver(post_save, sender=Match)
def handle_changes_on_add_or_update_match(sender, instance, created, **kwargs):
    if created:
        instance.round.matches_num += 1
        instance.round.save()
    else:
        update_predictions_points(instance)


@receiver(post_delete, sender=Match)
def handle_changes_on_delete_match(sender, instance, **kwargs):
    if instance.round.matches_num:
        instance.round.matches_num -= 1
        instance.round.save()


@receiver(post_save, sender=Round)
def handle_changes_on_add_or_update_round(sender, instance, created, **kwargs):
    if created:
        instance.tournament.rounds_num += 1
        instance.tournament.save()


@receiver(post_delete, sender=Round)
def handle_changes_on_delete_round(sender, instance, **kwargs):
    if instance.tournament.rounds_num:
        instance.tournament.rounds_num -= 1
        instance.tournament.save()


@receiver(post_delete, sender=Prediction)
def handle_changes_on_delete_prediction(sender, instance, **kwargs):
    instance.typer_card.predictions_num -= 1
    if instance.points:
        instance.typer_card.points -= instance.points
        instance.typer_card.save()


@receiver(post_save, sender=Prediction)
def handle_changes_on_save_prediction(sender, instance, created, **kwargs):
    if created:
        instance.typer_card.predictions_num += 1
        instance.typer_card.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
