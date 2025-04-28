from rest_framework import serializers
from .models import *


class PersonSerializer(serializers.ModelSerializer):
    church_description = serializers.ReadOnlyField(source='church.description')
    documenttype_description = serializers.ReadOnlyField(source='documenttype.description')

    class Meta:
        model = Person
        fields = '__all__'

class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = '__all__'

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'