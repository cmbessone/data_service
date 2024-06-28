from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

# from api.views import CSVUploadView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    # path("redocs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
