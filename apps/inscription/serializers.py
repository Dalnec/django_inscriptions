from rest_framework import serializers
from apps.person.serializers import PersonSerializer
from apps.person.models import Person
from .models import *


class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'


class InscriptionGroupCreateSerializer(serializers.ModelSerializer):
    people = PersonSerializer(many=True, write_only=True)
    voucherfile = serializers.ImageField(required=False)

    class Meta:
        model = InscriptionGroup
        fields = ['activity', 'voucheramount', 'voucherfile', 'vouchergroup', 
                'paymentmethod', 'tarifa', 'user', 'people']

    def create(self, validated_data):
        people_data = validated_data.pop("people")
        group = InscriptionGroup.objects.create(**validated_data)

        for person_data in people_data:
            doc_num = person_data.get("doc_num")
            person, _ = Person.objects.get_or_create(doc_num=doc_num, defaults=person_data)
            Inscription.objects.create(
                group=group,
                person=person,
                amount=group.voucheramount,  # o ajustado individualmente si es necesario
                status="P",
            )

        return group