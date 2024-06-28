from rest_framework import serializers
from base.models import Item, File


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("id", "file", "uploaded_at")  # Probar con all
