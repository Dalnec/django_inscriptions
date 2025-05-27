from rest_framework import serializers
from apps.person.serializers import PersonSerializer
from drf_extra_fields.fields import Base64ImageField
from apps.person.models import Person
from .models import *


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
    # voucherfile = serializers.ImageField(required=False)
    voucherfile = Base64ImageField(required=False)
    
    class Meta:
        model = InscriptionGroup
        fields = ['id','activity', 'voucheramount', 'voucherfile', 'vouchergroup', 
                'paymentmethod', 'tarifa', 'user', 'people']

    def create(self, validated_data):
        people_data = validated_data.pop("people")
        # Si la persona ya se encuentra registada en la actividad actual, no se debe crear una nueva inscripción
        already_registered = []
        for person in people_data:
            if Inscription.objects.filter(person__doc_num=person["doc_num"], group__activity=validated_data["activity"]).exists():
                already_registered.append(f"{person['doc_num']} {person['names']} {person['lastnames']}")
        if already_registered:
            raise serializers.ValidationError(f"Las siguientes personas ya están registradas en el evento actual: {', '.join(already_registered)}")
        
        # Validar que no existan personas con el mismo documento
        doc_nums = [person["doc_num"] for person in people_data]
        if len(doc_nums) != len(set(doc_nums)):
            raise serializers.ValidationError("Existen personas con el mismo documento.")
        
        # Si la persona ya se encuentra registada en el sistema
        validated_people = []
        for person in people_data:
            # p = Person.objects.filter(doc_num=person["doc_num"])
            # if p.exists():
            #     # actualizar nuevos valores
            #     p.update(**person)
            # else:
            #     # crear nueva persona
            #     Person.objects.create(**person)
            # update_or_create
            p, _ = Person.objects.update_or_create(doc_num=person["doc_num"], defaults=person)
            validated_people.append(p)

        group = InscriptionGroup.objects.create(**validated_data)

        for person_data in validated_people:
            # doc_num = person_data.get("doc_num")
            # person, _ = Person.objects.get_or_create(doc_num=doc_num, defaults=person_data)
            Inscription.objects.create(
                group=group,
                person=person_data, #person,
                amount=group.tarifa.price,  # o ajustado individualmente si es necesario
                status="P",
            )

        return group

class InscriptionGroupSerializer(serializers.ModelSerializer):
    tarifa = TarifaSerializer(read_only=True)
    paymentmethod = PaymentMethodSerializer(read_only=True)
    
    class Meta:
        model = InscriptionGroup
        fields = '__all__'


class InscriptionSerializer(serializers.ModelSerializer):
    group = InscriptionGroupSerializer(read_only=True)
    person = PersonSerializer(read_only=True)
    status_description = serializers.ReadOnlyField()


    class Meta:
        model = Inscription
        fields = '__all__'


class InscriptionSendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()