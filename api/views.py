from rest_framework.views import APIView
from django.views import View
from rest_framework.settings import api_settings
from rest_framework.parsers import FileUploadParser
from rest_framework_csv import renderers as r
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status 
from base.models import Item, File
from .serializers import ItemSerializer, FileSerializer
import pandas as pd
from django.shortcuts import render






class CSVUploadView(APIView):
    parser_classes = [FileUploadParser]
    # renderer_classes = (r.CSVRenderer,)
    template_name = 'uploads.html'

    def get(self, request, format=None):
        return render(request, self.template_name)

    def post(self, request, format=None):
        file_obj = request.data['file']
        if not file_obj:
            return Response("No file attached.", status=status.HTTP_400_BAD_REQUEST)
        
        filename = file_obj.name if hasattr(file_obj, 'name') else "uploaded_file.csv"
        try:
            df = pd.read_csv(file_obj)
            # Procesa el DataFrame según tus necesidades
            data = df.to_dict(orient='records')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getData(request):
	items = Item.objects.all()
	serializer = ItemSerializer(items, many =True)
	return Response(serializer.data)

@api_view(['POST'])
def addItem(request):
	serializer = ItemSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def file_upload_view(request):
    if request.method == 'POST':
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Method GET not allowed. Please use POST to upload a file."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
 