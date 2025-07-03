from django.urls import path
from .views import adherer,adherer_success

urlpatterns = [
    path('adherer/', adherer, name='adherer'),
     path('adherer/success/', adherer_success, name='adherer_success'),
]
