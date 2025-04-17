from django.core.management.base import BaseCommand
from apps.person.models import Church as NewChurch, DocumentType as NewDocumentType, Person as NewPerson
from apps.inscription.models import PaymentMethod as NewPaymentMethod, Tarifa as NewTarifa, InscriptionGroup, Inscription as NewInscription
from apps.activity.models import Activity as NewActivity
from apps.kenani.models import Church as Iglesias, Documenttype as TipoDoc, Inscription as Inscripcion, Paymentmethod as MetodoPago, Person as Persona

class Command(BaseCommand):
    help = "Extrae datos desde la base externa y los inserta en el sistema local"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("🔄 Iniciando proceso de seed...")

            # Actividades
            newactity = NewActivity.objects.create(
                title="Actividad de prueba",
                description="Descripción de prueba",
                location="Ubicación de prueba",
                start_date="2023-01-01 00:00:00",
                end_date="2023-01-02 00:00:00",
                is_active=True,
            )
            
            # Iglesias
            iglesias = Iglesias.objects.using('externa').all()
            NewChurch.objects.all().delete()
            new_iglesias = [NewChurch(description=i.description, active=i.active) for i in iglesias]
            NewChurch.objects.bulk_create(new_iglesias)
            self.stdout.write(f"✅ Iglesias importadas: {len(new_iglesias)}")

            # Tipos de documento
            tipos_doc = TipoDoc.objects.using('externa').all()
            NewDocumentType.objects.all().delete()
            new_docs = [NewDocumentType(description=d.description, active=d.active) for d in tipos_doc]
            NewDocumentType.objects.bulk_create(new_docs)
            self.stdout.write(f"✅ Documentos importados: {len(new_docs)}")

            # Métodos de pago
            metodos_pago = MetodoPago.objects.using('externa').all()
            NewPaymentMethod.objects.all().delete()
            new_pagos = [
                NewPaymentMethod(description=m.description, account=m.account, icon=m.icon, active=m.active)
                for m in metodos_pago
            ]
            NewPaymentMethod.objects.bulk_create(new_pagos)
            self.stdout.write(f"✅ Métodos de pago importados: {len(new_pagos)}")

            # Personas
            personas = Persona.objects.using('externa').all()
            NewPerson.objects.all().delete()
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
                        birthday=persona.birthday,
                        phone=persona.phone,
                        email=persona.email,
                        status=persona.status,
                        kind=persona.type_person,
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
            NewInscription.objects.all().delete()
            InscriptionGroup.objects.all().delete()
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
                        activity=newactity,  # Asegúrate de que exista y se pueda mapear
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
