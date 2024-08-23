from django.apps import AppConfig
from background_task import background

class ReservationsConfig(AppConfig):
    name = 'reservations'

    def ready(self):
        @background(schedule=1)
        def run_daily_routine():
            from .views import update_clients_and_garage
            update_clients_and_garage()
