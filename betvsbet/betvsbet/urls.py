from django.contrib import admin
from django.urls import path, include
from betvsbet import settings
from tour import views
from tour.views import page_not_found
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tour.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Турниры"
