from django.urls import path
from . import views

urlpatterns = [
    path('', views.opening_view, name='opening_view'),  # URL racine de l'application
    path('variations/<int:opening_id>/', views.get_variations, name='get_variations'),
]