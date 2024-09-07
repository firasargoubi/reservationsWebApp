from django.conf import settings
from reservations.views import update_clients_and_garage
def job() :
    update_clients_and_garage()
