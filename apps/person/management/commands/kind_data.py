from django.core.management.base import BaseCommand
from apps.person.models import Kind, Person

class Command(BaseCommand):
    help = "Actualiza el campo kind_fk en la tabla Person según el campo kind"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Iniciando proceso de actualización de kind_fk...")

        self.stdout.write("Llenando Opciones Kind")
        kinds = [
            Kind(description="Lider", active=True),
            Kind(description="Pastor", active=True),
            Kind(description="Miembro Activo", active=True),
            Kind(description="Invitado", active=True),
        ]
        for kind in kinds:
            Kind.objects.get_or_create(
                description=kind.description,
                defaults={"active": kind.active}
            )
        self.stdout.write(f"✅ Opciones Kind creadas: {len(kinds)}")

        default_kind = Kind.objects.get(description="Miembro Activo")

        # Mapeo de valores de kind a descripciones de Kind
        kind_mapping = {
            'L': 'Lider',
            'P': 'Pastor',
            'M': 'Miembro Activo',
            'I': 'Invitado',
        }

        for person in Person.objects.all():
            if person.kind in kind_mapping:
                kind_obj = Kind.objects.get(description=kind_mapping[person.kind])
                person.kind_fk = kind_obj
                person.save()
            else:
                # Si el valor de kind no está en el mapeo, asignar el valor por defecto
                person.kind_fk = default_kind
                person.save()

        self.stdout.write("✅ Proceso de actualización de kind_fk completado.")