from rest_framework.views import APIView
from django.views import View
from rest_framework.settings import api_settings
from rest_framework.parsers import FileUploadParser
from rest_framework_csv import renderers as r
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status 
from base.models import Item, File
from .serializers import ItemSerializer, FileSerializer
import pandas as pd
import numpy as np
from django.shortcuts import render
from pymongo import MongoClient
from django.urls import reverse


#MENU VIEW

class MenuView(View):
    def get(self, request):
        # Define aquí las URLs y nombres para tus APIs
        api_endpoints = [
            {'url': reverse('upload'), 'name': 'CSV Upload API'},
            {'url': reverse('data-list'), 'name': 'Data List API'},
            # Agrega aquí más APIs
        ]

        return render(request, 'menu.html', {'api_endpoints': api_endpoints})



# UPLOAD CSV API
class DataListView(APIView):
    def get(self, request, collection_name=None, format=None):
        try:
            client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
            db = client[settings.MONGODB_DATABASE_NAME]
            
            if collection_name:
                collection = db[collection_name]
                documents = list(collection.find({}))  # Query all documents from specified MongoDB collection
                df = pd.DataFrame(documents)
            else:
                # If no collection_name is provided, fetch all collections or handle as needed
                # For illustration, fetch all collections and show the first one
                collections = db.list_collection_names()
                if collections:
                    collection = db[collections[0]]
                    documents = list(collection.find({}))
                    df = pd.DataFrame(documents)
                else:
                    # Handle case where there are no collections
                    df = pd.DataFrame()

            # Convert DataFrame to HTML table
            table_html = df.to_html(classes='table table-bordered', index=False)

            context = {
                'table_html': table_html,
                'collection_name': collection_name if collection_name else 'All Collections'  # Display collection name or indicate all collections
            }

            client.close()

            return render(request, 'data_table.html', context)
        
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# Define the CSVUploadView class as a subclass of APIView
class CSVUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    template_name = 'uploads.html'

    def get(self, request, format=None):
        return render(request, self.template_name)

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        collection_name = request.POST.get('collection_name')

        if not file_obj:
            return Response("No file attached.", status=status.HTTP_400_BAD_REQUEST)
        
        if not collection_name:
            return Response("No collection name provided.", status=status.HTTP_400_BAD_REQUEST)
       
        try:
            df = pd.read_csv(file_obj)
            df.fillna(value="", inplace=True)

            self.insert_dataframe_to_mongodb(df, collection_name)

            return Response("Data saved successfully", status=status.HTTP_201_CREATED)

        except pd.errors.EmptyDataError:
            return Response("Empty file provided.", status=status.HTTP_400_BAD_REQUEST)

        except pd.errors.ParserError as e:
            return Response(f"Error parsing CSV file: {str(e)}", status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def insert_dataframe_to_mongodb(self, df, collection_name):
        try:
            client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
            db = client[settings.MONGODB_DATABASE_NAME]
            collection = db[collection_name]

            # Convert DataFrame records to a list of dictionaries
            data = df.to_dict(orient='records')

            # Insert records into MongoDB collection
            collection.insert_many(data)

        finally:
            client.close()



# ITEM API

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
 