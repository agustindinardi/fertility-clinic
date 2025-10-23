from django.urls import path
from . import views

urlpatterns = [
    path('', views.treatment_list, name='treatment_list'),
    path('my-treatments/', views.my_treatments, name='my_treatments'),
    path('<int:treatment_id>/', views.treatment_detail, name='treatment_detail'),
    path('initiate/<int:patient_id>/', views.initiate_treatment, name='initiate_treatment'),
    path('<int:treatment_id>/add-study/', views.add_study_result, name='add_study_result'),
    path('<int:treatment_id>/update-protocol/', views.update_stimulation_protocol, name='update_stimulation_protocol'),
    path('<int:treatment_id>/assign-monitoring/', views.assign_monitoring_days, name='assign_monitoring_days'),
    path('<int:treatment_id>/create-order/', views.create_medical_order, name='create_medical_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
