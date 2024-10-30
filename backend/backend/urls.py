from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
    path('initiatives/', include('initiatives.urls')),
    path('accounts/', include('accounts.urls')),  # маршруты аутентификации
    
]
if settings.DEBUG:  # Это нужно только в режиме разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)