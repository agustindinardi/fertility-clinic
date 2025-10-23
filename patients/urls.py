from django.urls import path
from . import views

urlpatterns = [
    path('complete-profile/', views.complete_patient_profile, name='complete_patient_profile'),
    path('list/', views.patient_list, name='patient_list'),
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),
]
