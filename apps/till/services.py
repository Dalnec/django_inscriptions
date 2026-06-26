from django.db.models import Case, Count, DecimalField, F, Sum, Value, When
from django.db.models.functions import Coalesce
from rest_framework import serializers

from .models import Concept, ConceptType, Movement, MovementStatus


def get_cash_balance(activity=None):
    """
    Retorna el saldo de caja.
    Opcionalmente filtra por actividad.
    Retorna: { total_incomes, total_expenses, cash_total, movement_count }
    """
    queryset = Movement.objects.filter(status=MovementStatus.POSTED)
    if activity:
        queryset = queryset.filter(activity=activity)

    totals = queryset.aggregate(
        total_incomes=Coalesce(
            Sum(
                Case(
                    When(concept__concept_type="I", then=F("amount")),
                    default=Value(0),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ),
            Value(0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        total_expenses=Coalesce(
            Sum(
                Case(
                    When(concept__concept_type="E", then=F("amount")),
                    default=Value(0),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ),
            Value(0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        movement_count=Count("id"),
    )
    totals["cash_total"] = totals["total_incomes"] - totals["total_expenses"]
    return totals


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
