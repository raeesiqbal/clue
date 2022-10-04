from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("", include("clue.urls")),
    path("admin/", admin.site.urls),
    path("celery-progress/", include("celery_progress.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
