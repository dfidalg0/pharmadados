from django.apps import AppConfig


class MedicinesConfig(AppConfig):
    name = 'medicines'

    def ready(self):
        from .db_update import run
        from os import environ

        if environ.get('RUN_MAIN', None) == 'true':
            run()
