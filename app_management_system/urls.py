from django.contrib import admin
from django.urls import path, include
from app_management_system.core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('applications/', include('app_management_system.applications.urls')),
    path('reviewers/', include('app_management_system.reviewer.urls')),
    path('', include('app_management_system.core.urls')),
    path('', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
