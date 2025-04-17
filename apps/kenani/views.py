from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.person.models import Church as NewChurch, DocumentType as NewDocumentType, Person as NewPerson
from apps.inscription.models import PaymentMethod as NewPaymentMethod, Tarifa as NewTarifa, InscriptionGroup, Inscription as NewInscription
from apps.seed.serializers import SeedSerializer
from .models import Church as Iglesias, Documenttype as TipoDoc, Inscription as Inscripcion, Paymentmethod as MetodoPago, Person as Persona

# @extend_schema(tags=['Extracting'])
# class ExtractingDataViewSet(GenericViewSet):
#     serializer_class = SeedSerializer

#     def create(self, request, *args, **kwargs):
#         # try:
#         churches = Iglesias.objects.using('externa').all()
#         docstype = TipoDoc.objects.using('externa').all()
#         inscriptions = Inscripcion.objects.using('externa').all()
#         paymentsmethods = MetodoPago.objects.using('externa').all()
#         people = Persona.objects.using('externa').all().order_by('id')
        
#         for church in churches:
#             print(church.description, church.active)
#             NewChurch.objects.create(
#                 description=church.description,
#                 active=church.active
#             )
        
#         for doc in docstype:
#             print(doc.description, doc.active)
#             NewDocumentType.objects.create(
#                 description=doc.description,
#                 active=doc.active
#             )
        
#         for payment in paymentsmethods:
#             print(payment.description, payment.account, payment.icon, payment.active)
#             NewPaymentMethod.objects.create(
#                 description=payment.description,
#                 account=payment.account,
#                 icon=payment.icon,
#                 active=payment.active
#             )
        
#         for person in people:
#             print(person.doc_num, person.names, person.lastnames, person.birthday, person.phone, person.email, person.status, person.type_person, person.documenttype, person.church)
#             dt = NewDocumentType.objects.get(id=person.documenttype.id)
#             church = NewChurch.objects.get(id=person.church.id)
#             p = NewPerson.objects.create(
#                 created=person.created,
#                 modified=person.modified,
#                 code=person.code,
#                 doc_num=person.doc_num,
#                 names=person.names,
#                 lastnames=person.lastnames,
#                 gender=person.gender,
#                 birthday=person.birthday,
#                 phone=person.phone,
#                 email=person.email,
#                 status=person.status,
#                 kind=person.type_person,
#                 documenttype=dt,
#                 church=church
#             )
#             p.generate_code()

#         for inscription in inscriptions:
#             person = NewPerson.objects.get(id=inscription.person.id)
#             payment = NewPaymentMethod.objects.get(id=inscription.paymentmethod.id)

#             InscriptionGroup.objects.create(
#                 vouchergroup=inscription.vouchergroup,
#                 voucherfile=inscription.voucherfile,
#                 voucheramount=inscription.voucheramount,
#                 # activity=inscription.activity,
#                 # user=inscription.user,
#                 paymentmethod=inscription.paymentmethod,
#                 tarifa=inscription.tarifa
#             )
            
#             NewInscription.objects.create(
#                 created=inscription.created,
#                 modified=inscription.modified,
#                 status=inscription.status,
#                 amount=inscription.amount,
#                 observations=inscription.observations,
#                 group=inscription.group,
#                 person=inscription.person,
#             )


#         return Response('Seeding Completed!', status=status.HTTP_200_OK)

#         # except Exception as e:
#         #     return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)