
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('apropos/', include('apropos.urls')),
    path('app/', include('app.urls')),
    path('temoin/',include('temoin.urls')),
    path('documents/', include('documents.urls')),
    path('events/', include('events.urls')),
    path('adherents/',include('adherents.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
