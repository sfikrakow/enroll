from django.urls import path
from . import views

app_name = 'workshop'

urlpatterns = [
    path('',views.index)
]