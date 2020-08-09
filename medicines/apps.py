from django.apps import AppConfig


class MedicinesConfig(AppConfig):
    name = 'medicines'

    def ready(self):
        from .db_update import run
        import os

        if os.environ.get('UPDATE_DB', '') == 'true':
            run()
