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



# UPLOAD CSV API
class DataListView(APIView):
    def get(self, request, format=None):
        try:
            client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
            db = client[settings.MONGODB_DATABASE_NAME]
            collection_name = 'uploaded_data'
            collection = db[collection_name]

            if db is None:
                return Response("Database connection failed.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            documents = list(collection.find({}))  # Query all documents from MongoDB

            # Convert MongoDB documents to DataFrame
            df = pd.DataFrame(documents)

            # Convert DataFrame to HTML table
            table_html = df.to_html(classes='table table-bordered', index=False)

            context = {
                'table_html': table_html
            }

            client.close()

            return render(request, 'data_table.html', context)
        
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



# Define the CSVUploadView class as a subclass of APIView
class CSVUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Specify parser classes for file upload
    template_name = 'uploads.html'  # Template name for rendering (optional)

    # GET request handler to render an HTML form (optional)
    def get(self, request, format=None):
        return render(request, self.template_name)

    # POST request handler to process CSV file upload
    def post(self, request, format=None):
        file_obj = request.FILES.get('file')  # Retrieve uploaded file from request

        if not file_obj:
            return Response("No file attached.", status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file_obj)  # Read CSV file into pandas DataFrame
            df.fillna(value="", inplace=True)  # Fill NaN values with empty string (optional)

            collection_name = 'uploaded_data'  # MongoDB collection name

            # Insert DataFrame records into MongoDB collection
            self.insert_dataframe_to_mongodb(df, collection_name)

            return Response("Data saved successfully", status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    # Method to insert DataFrame records into MongoDB collection
    def insert_dataframe_to_mongodb(self, df, collection_name):
        # Connect to MongoDB (adjust connection details as needed)
        client = MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
        db = client[settings.MONGODB_DATABASE_NAME]
        collection = db[collection_name]

        if db is None:
            raise ValueError("Failed to connect to the database.")

        # Convert DataFrame records to a list of dictionaries
        data = df.to_dict(orient='records')

        # Insert records into MongoDB collection
        collection.insert_many(data)

        # Close MongoDB connection
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
 