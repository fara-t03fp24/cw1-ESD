from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Error handlers
handler404 = 'apps.weather.views.custom_404'
handler500 = 'apps.weather.views.custom_500'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.weather.urls')),  # Weather URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
