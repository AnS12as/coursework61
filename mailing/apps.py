from django.apps import AppConfig
import time


class MailingConfig(AppConfig):
    name = 'mailing'

    def ready(self):
        from . import scheduler
        time.sleep(2)
        scheduler.start()

