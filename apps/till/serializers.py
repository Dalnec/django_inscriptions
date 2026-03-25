from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Concept, Movement


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = "__all__"


class MovementSerializer(serializers.ModelSerializer):
    concept_description = serializers.CharField(source="concept.description", read_only=True)
    concept_type = serializers.CharField(source="concept.concept_type", read_only=True)
    signed_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Movement
        fields = "__all__"
        read_only_fields = ("created", "modified")

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)
