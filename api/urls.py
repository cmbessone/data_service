from django.urls import path
from . import views
from .views import CSVUploadView


urlpatterns = [
	path('', views.getData),
	path('add/',views.addItem),
	path('upload/',views.CSVUploadView.as_view(), name='upload')

	# path('upload/', CSVUploadView.as_view(), name='file_upload_view'),

]