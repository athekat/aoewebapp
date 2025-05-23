# match1v1/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='match1v1-home'),
]
