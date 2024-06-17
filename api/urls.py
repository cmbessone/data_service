from django.urls import path
from rest_framework.schemas import get_schema_view

from . import views





urlpatterns = [
    #path('', views.getData),
    path(
    	'openapi', get_schema_view(title='myproject',description='API for SPO'),
    	name='upload',),
    path('', views.MenuView.as_view(), name='menu'),
    path('add/', views.addItem),
    path('upload/', views.CSVUploadView.as_view(), name='upload'),
    path('data-list/', views.DataListView.as_view(), name='data-list'),  # Ruta sin parámetros
    path('data-list/<str:collection_name>/', views.DataListView.as_view(), name='data-list-param'),  # Ruta con parámetro
    path('docs/', get_schema_view(title='myproject',description='API for SPO')),
]
