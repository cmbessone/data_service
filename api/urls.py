from django.urls import path
from . import views



urlpatterns = [
	path('', views.getData),
	path('add/',views.addItem),
	path('upload/',views.CSVUploadView.as_view(), name='upload'),
	path('data-list/', views.DataListView.as_view(), name='data-list'),
	
	
]