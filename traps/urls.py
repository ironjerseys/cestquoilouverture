from django.urls import path
from . import views

urlpatterns = [
    path('', views.traps_view, name='traps_view'),  # URL racine de l'application
]