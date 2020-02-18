from django.urls import path
from . import views

app_name = 'workshop'

urlpatterns = [
    path('', views.index),
    path('<int:idx>/', views.register_form, name='register_form'),
    path('registrations/', views.my_registrations, name='my_registrations'),
    path('unregister/', views.unregister_form, name='unregister_form'),
]
