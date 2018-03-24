from __future__ import unicode_literals

from django.apps import AppConfig


class TypersConfig(AppConfig):
    name = 'typers'
    varbose_name = 'Typers'

    def ready(self):
        import typers.signals.handlers
