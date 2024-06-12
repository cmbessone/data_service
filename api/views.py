from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from base.models import Item, File
from .serializers import ItemSerializer, FileSerializer

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
def file_upload_view(request):
    if request.method == 'POST':
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)