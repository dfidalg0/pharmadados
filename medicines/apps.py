from django.apps import AppConfig


class MedicinesConfig(AppConfig):
    name = 'medicines'

    def ready(self):
        from .db_update import run
        from sys import argv

        if '--noreload' in argv:
            run()
