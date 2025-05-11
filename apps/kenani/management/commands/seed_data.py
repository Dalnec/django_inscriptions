from django.core.management.base import BaseCommand
from apps.person.models import Church as NewChurch, DocumentType as NewDocumentType, Person as NewPerson, Kind
from apps.inscription.models import PaymentMethod as NewPaymentMethod, Tarifa as NewTarifa, InscriptionGroup, Inscription as NewInscription
from apps.activity.models import Activity as NewActivity
from apps.kenani.models import Church as Iglesias, Documenttype as TipoDoc, Inscription as Inscripcion, Paymentmethod as MetodoPago, Person as Persona

class Command(BaseCommand):
    help = "Extrae datos desde la base externa y los inserta en el sistema local"

    def get_kind(self, kind):
        if kind == "P":
            return Kind.objects.get(description="PASTOR")
        elif kind == "L":
            return Kind.objects.get(description="LIDER")
        elif kind == "M":
            return Kind.objects.get(description="MIEMBRO ACTIVO")
        elif kind == "I":
            return Kind.objects.get(description="INVITADO")
        else:
            return None 
    
    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("🔄 Iniciando proceso de seed...")

            # Actividades
            newactivity = NewActivity.objects.create(
                title="Actividad de prueba",
                description="Descripción de prueba",
                location="Ubicación de prueba",
                start_date="2023-01-01 00:00:00",
                end_date="2023-01-02 00:00:00",
                is_active=False,
            )
            newactivity2 = NewActivity.objects.create(
                title="KASOSH",
                description="Campamento de jóvenes",
                location="Tarapoto - Lamas",
                start_date="2023-01-01 00:00:00",
                end_date="2023-01-02 00:00:00",
                is_active=True,
            )
            self.stdout.write(f"✅ Actividad creada: {newactivity.title}")
            self.stdout.write(f"✅ Actividad creada: {newactivity2.title}")
            # Kind
            kind_data = [
                Kind(description="PASTOR", active=True), 
                Kind(description="LIDER", active=True),
                Kind(description="MIEMBRO ACTIVO", active=True),
                Kind(description="INVITADO", active=True)
            ]
            Kind.objects.bulk_create(kind_data)
            self.stdout.write(f"✅ Kinds creados: {len(kind_data)}")

            # Tarifas
            tarifas = [ { "id": 1, "description": "GENERAL", "price": 120, "selected": True, }, { "id": 2, "description": "ALIMENTACION Y TALLERES", "price": 90, "selected": False, }, { "id": 3, "description": "HOSPEDAJE Y TALLERES", "price": 60, "selected": False, }, { "id": 4, "description": "4 DÍAS", "price": 110, "selected": False, }, { "id": 5, "description": "3 DÍAS", "price": 80, "selected": False, }, { "id": 6, "description": "2 DÍAS", "price": 50, "selected": False, }, { "id": 7, "description": "1 DÍA", "price": 25, "selected": False, }, { "id": 8, "description": "TALLERES", "price": 40, "selected": False, }, { "id": 9, "description": "OTRO MONTO", "price": 0, "selected": False, }, ]
            # NewTarifa.objects.all().delete()
            new_tarifas = [NewTarifa(id=t["id"], description=t["description"], price=t["price"], selected=t["selected"]) for t in tarifas]
            NewTarifa.objects.bulk_create(new_tarifas)
            self.stdout.write(f"✅ Tarifas creadas: {len(new_tarifas)}")

            
            # Iglesias
            iglesias = Iglesias.objects.using('externa').all()
            # NewChurch.objects.all().delete()
            new_iglesias = [NewChurch(description=i.description, active=i.active) for i in iglesias]
            NewChurch.objects.bulk_create(new_iglesias)
            self.stdout.write(f"✅ Iglesias importadas: {len(new_iglesias)}")

            # Tipos de documento
            tipos_doc = TipoDoc.objects.using('externa').all()
            # NewDocumentType.objects.all().delete()
            new_docs = [NewDocumentType(description=d.description, active=d.active) for d in tipos_doc]
            NewDocumentType.objects.bulk_create(new_docs)
            self.stdout.write(f"✅ Documentos importados: {len(new_docs)}")

            # Métodos de pago
            metodos_pago = MetodoPago.objects.using('externa').all()
            # NewPaymentMethod.objects.all().delete()
            new_pagos = [
                NewPaymentMethod(description=m.description, account=m.account, active=m.active)
                for m in metodos_pago
            ]
            NewPaymentMethod.objects.bulk_create(new_pagos)
            self.stdout.write(f"✅ Métodos de pago importados: {len(new_pagos)}")

            # Personas
            personas = Persona.objects.using('externa').all()
            # NewPerson.objects.all().delete()
            count_personas = 0
            for persona in personas:
                try:
                    doc_type = NewDocumentType.objects.get(description=persona.documenttype.description)
                    church = NewChurch.objects.get(description=persona.church.description)
                    p = NewPerson.objects.create(
                        created=persona.created,
                        modified=persona.modified,
                        code=persona.code,
                        doc_num=persona.doc_num,
                        names=persona.names,
                        lastnames=persona.lastnames,
                        gender=persona.gender,
                        birthdate=persona.birthday,
                        phone=persona.phone,
                        email=persona.email,
                        status=persona.status,
                        kind=self.get_kind(persona.type_person),
                        documenttype=doc_type,
                        church=church
                    )
                    p.generate_code()
                    count_personas += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️ Error en persona {persona.id}: {str(e)}"))
            self.stdout.write(f"✅ Personas importadas: {count_personas}")

            # Inscripciones
            inscripciones = Inscripcion.objects.using('externa').all()
            # NewInscription.objects.all().delete()
            # InscriptionGroup.objects.all().delete()
            count_inscripciones = 0
            for ins in inscripciones:
                try:
                    person = NewPerson.objects.get(doc_num=ins.personid.doc_num)
                    payment = NewPaymentMethod.objects.get(description=ins.paymentmethodid.description)
                    group = InscriptionGroup.objects.create(
                        vouchergroup=ins.vouchergroup,
                        voucherfile=ins.voucherpath,
                        voucheramount=ins.voucheramount,
                        paymentmethod=payment,
                        activity=newactivity,  # Asegúrate de que exista y se pueda mapear
                        # tarifa=ins.tarifa  # Asegúrate de que exista y se pueda mapear
                    )
                    NewInscription.objects.create(
                        created=ins.created,
                        modified=ins.modified,
                        status=ins.status,
                        amount=ins.amount,
                        observations=ins.observations,
                        group=group,
                        person=person,
                    )
                    count_inscripciones += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️ Error en inscripción {ins.id}: {str(e)}"))

            self.stdout.write(f"✅ Inscripciones importadas: {count_inscripciones}")
            self.stdout.write(self.style.SUCCESS("🎉 Proceso completado con éxito"))

        except Exception as e:
            import traceback
            self.stderr.write(self.style.ERROR("❌ Error general al importar datos"))
            self.stderr.write(self.style.ERROR(str(e)))
            self.stderr.write(traceback.format_exc())
