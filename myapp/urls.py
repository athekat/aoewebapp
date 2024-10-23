from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.my_view, name='my_view'),
]
