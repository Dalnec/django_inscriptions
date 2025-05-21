import re
from rest_framework import serializers
from .models import *


class PersonSerializer(serializers.ModelSerializer):
    church_description = serializers.ReadOnlyField(source='church.description')
    documenttype_description = serializers.ReadOnlyField(source='documenttype.description')
    kind_description = serializers.ReadOnlyField(source='kind.description')

    class Meta:
        model = Person
        fields = '__all__'
    
    def validate_doc_num(self, value):
        if not re.match(r'^\d+$', value):
            raise serializers.ValidationError("El documento solo puede contener números.")
        if not value:
            raise serializers.ValidationError("El documento no puede estar vacío.")
        
        # # Validación para CREATE: Evita duplicados en creación
        # if self.instance is None and Person.objects.filter(doc_num=value).exists():
        #     raise serializers.ValidationError("Ya existe una persona con este documento.")
        
        # # Validación para UPDATE: Evita duplicados al actualizar (excepto en sí misma)
        # if self.instance and Person.objects.filter(doc_num=value).exclude(id=self.instance.id).exists():
        #     raise serializers.ValidationError("Ya existe otra persona con este documento.")
        
        return value

class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = '__all__'

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'