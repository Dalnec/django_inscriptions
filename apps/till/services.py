from rest_framework import serializers

from .models import Concept, ConceptType, Movement, MovementStatus


def create_inscription_group_movement(group):
    concept = Concept.objects.filter(
        description__iexact="INSCRIPCION",
        concept_type=ConceptType.INCOME,
        is_active=True,
    ).first()
    if concept is None:
        raise serializers.ValidationError(
            {
                "cash": (
                    "No existe un concepto activo de ingreso con descripcion "
                    "'INSCRIPCION'."
                )
            }
        )

    movement, _ = Movement.objects.get_or_create(
        inscription_group=group,
        defaults={
            "description": f"Ingreso por inscripcion {group.vouchergroup}",
            "reference": group.vouchergroup,
            "amount": group.voucheramount,
            "status": MovementStatus.POSTED,
            "concept": concept,
            "payment_method": group.paymentmethod,
            "user": group.user,
            "activity": group.activity,
        },
    )
    return movement
