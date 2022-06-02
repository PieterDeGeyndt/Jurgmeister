from django.urls import path
from . import views

urlpatterns = [
    path('',views.allservices, name='allservices'),
    path('<int:service_id>/', views.servicedetail, name='servicedetail'),
    path('pripol/',views.pripol, name='pripol'),
    ]