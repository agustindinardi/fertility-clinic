from django.urls import path
from . import views

urlpatterns = [
    path('puncture/', views.puncture_list, name='puncture_list'),
    path('puncture/register/<int:treatment_id>/', views.register_puncture, name='register_puncture'),
    path('puncture/<int:puncture_id>/', views.puncture_detail, name='puncture_detail'),
    path('puncture/<int:puncture_id>/add-oocyte/', views.add_oocyte, name='add_oocyte'),
    path('oocyte/', views.oocyte_list, name='oocyte_list'),
    path('oocyte/<int:oocyte_id>/', views.oocyte_detail, name='oocyte_detail'),
    path('oocyte/<int:oocyte_id>/update/', views.update_oocyte, name='update_oocyte'),
    path('oocyte/<int:oocyte_id>/create-embryo/', views.create_embryo, name='create_embryo'),
    path('embryo/', views.embryo_list, name='embryo_list'),
    path('embryo/<int:embryo_id>/', views.embryo_detail, name='embryo_detail'),
    path('embryo/<int:embryo_id>/update/', views.update_embryo, name='update_embryo'),
    path('embryo/<int:embryo_id>/schedule-transfer/', views.schedule_transfer, name='schedule_transfer'),
    path('my-biological-products/', views.my_biological_products, name='my_biological_products'),
]
