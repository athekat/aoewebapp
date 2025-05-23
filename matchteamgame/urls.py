from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='match4v4-home'),
]
