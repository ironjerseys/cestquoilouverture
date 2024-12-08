from django.urls import path
from . import views

urlpatterns = [
    path('', views.opening_view, name='opening_view'),  # URL racine de l'application
]