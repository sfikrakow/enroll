from django.urls import path
from . import views

app_name = 'workshop'

urlpatterns = [
    path('', views.index),
    path('<int:idx>/', views.register_form, name='register_form'),
    path('registrations/', views.my_registrations, name='my_registrations'),
    path('unregister/', views.unregister_form, name='unregister_form'),
    path('manage_reg/', views.manage_reg, name='manage_registrations'),
    path('manage_reg/<int:idx>', views.load_regs, name='manage_registrations_id')
]
