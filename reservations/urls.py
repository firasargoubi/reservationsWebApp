from django.urls import path
from . import views

urlpatterns = [
    path("",views.calendar, name="calendar"),
    path('reservations/', views.make_reservation, name= "reservations"),
    path('timeline/',views.timeline,name="timeline"),
    path('delete_admin/',views.delete_client, name="delete_admin"),
    path('delete_reservation/<int:id>',views.delete_page,name="delete_reservation"),
    path('validate/',views.validate_user, name = "validate"),
    path('invalidate/',views.invalidate_user, name = "invalidate")
]