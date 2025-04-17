import json
from tablib import Dataset
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.kenani.models import *
# from ..ubigeo.admin import DepartmentResource, ProvinceResource, DistrictResource
# from ..business.models import Business, Branch
# from ..credit.models import PaymentMethod
# from ..user.models import Profile

from .serializers import SeedSerializer
# from apps.user.serializers import UserSerializer, EmployeeSerializer

from tablib import Dataset
import json

@extend_schema(tags=['Seeding'])
class SeedingDataViewSet(GenericViewSet):
    serializer_class = SeedSerializer

    def create(self, request, *args, **kwargs):

        try:
            # file_resources = {
            #     'apps/seed/data/Department.json': DepartmentResource(),
            #     'apps/seed/data/Province.json': ProvinceResource(),
            #     'apps/seed/data/District.json': DistrictResource(),
            # }

            # obj, created = Business.objects.get_or_create(
            #     id=1, 
            #     ruc="20604462542",
            #     name="FINAMERICA EIRL",
            #     commercial_name="FINAMERICA EIRL",
            #     fiscal_address="Jr 2 de mayo M.° 799",
            #     legal_representative="El dueño"
            # )
            # Branch.objects.get_or_create(
            #     id=1,
            #     description="MOYOBAMBA",
            #     commercial_address="Jr. Dos de Mayo N° 799",
            #     business=obj,
            # )
            # PaymentMethod.objects.get_or_create( id=1, description="EFECTIVO" )
            # PaymentMethod.objects.get_or_create( id=2, description="TRANSFERENCIA" )
            # Profile.objects.get_or_create( id=1, description="SOCIO" )
            # Profile.objects.get_or_create( id=2, description="COBRADOR" )
            # Profile.objects.get_or_create( id=3, description="REVISADOR" )

            # for file_path, resource_model in file_resources.items():
            #     dataset = Dataset()

            #     with open(file_path, 'r', encoding='utf-8') as json_file:
            #         json_data = json.load(json_file)
            #         dataset.dict = json_data

            #     result = resource_model.import_data(dataset, dry_run=False)

            #     if result.has_errors():
            #         errors = result.row_errors()
            
            # data_admin = {
            #     "names": "ADMINISTRADOR",
            #     "lastnames": "BIERY",
            #     "dni": "88888888",
            #     "address": "Su casa",
            #     "phone": "987654321",
            #     "pincode": "1234",
            #     "email": "biery@biery.pe",
            #     "commission": "1.96",
            #     "total_commission": "1.96",
            #     "branch": 1,
            #     "is_active": True,
            #     "username": "ADMINISTRADOR",
            #     "is_staff": True,
            #     "is_active": True,
            #     "is_owner": True,
            #     "password": "123456"
            # }

            # user_serializer = UserSerializer(data=data_admin)
            # user_serializer.is_valid(raise_exception=True)
            # user = user_serializer.save()
            # serializer = EmployeeSerializer(data=data_admin)
            # serializer.is_valid(raise_exception=True)
            # serializer.save(user=user)
            
            return Response('Seeding Completed!', status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
