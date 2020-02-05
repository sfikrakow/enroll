from django.urls import path
from . import views

app_name = 'workshop'

urlpatterns = [
    path('', views.index),
    path('register/<int:idx>/', views.register_form, name='register_form'),
]
