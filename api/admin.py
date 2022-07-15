from django.conf import settings
from django.contrib import admin

admin.site.site_header = f"{settings.APP_NAME} Administration"
admin.site.site_title = f"{settings.APP_NAME} Admin"
