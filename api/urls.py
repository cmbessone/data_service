from django.urls import path
from rest_framework.schemas import get_schema_view
from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="SPO Platform",
        default_version="v1",
        description="Data Service",
        terms_of_service="https://www.sponsorsconnection.com/",
        contact=openapi.Contact(email="cristian@spo.com"),
        license=openapi.License(name="SPO License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('', views.getData),
    path("", views.MenuView.as_view(), name="menu"),
    path("add/", views.addItem),
    path("upload/", views.CSVUploadView.as_view(), name="upload"),
    path(
        "data-list/", views.DataListView.as_view(), name="data-list"
    ),  # Ruta sin parámetros
    path(
        "data-list/<str:collection_name>/",
        views.DataListView.as_view(),
        name="data-list-param",
    ),  # Ruta con parámetro
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
