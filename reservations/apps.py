from django.apps import AppConfig

class MainConfig(AppConfig) :
    default_auto_field = 'django.db.models.AutoField'
    name = 'reservations'

    def ready(self) :
        from jobs import updater
        updater.start()
