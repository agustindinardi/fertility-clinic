from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointments/', views.appointments_placeholder, name='appointments'),
    path('calendar/', views.calendar_placeholder, name='calendar_placeholder'),
    path('payments/', views.payments_placeholder, name='payments'),
    path('notifications/', views.notifications_placeholder, name='notifications_placeholder'),
    path('patient-treatments/', views.patient_treatments, name='patient_treatments'),
    path('patient-orders/', views.patient_orders, name='patient_orders'),
]
