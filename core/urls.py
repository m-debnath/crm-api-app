from django.conf import settings
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = f"{settings.APP_NAME} Administration"
admin.site.site_title = f"{settings.APP_NAME} Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
