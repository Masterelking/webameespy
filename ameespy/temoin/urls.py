from django.urls import path
from .views import temoignage_list

urlpatterns = [
    path('temoignages/', temoignage_list, name='temoin'),
]
