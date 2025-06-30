from django.urls import path
from . import views

urlpatterns = [
    path('', views.laporan_cuti, name='laporan_cuti'),
]