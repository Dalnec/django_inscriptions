from django.db import transaction
from rest_framework import serializers

from apps.till.models import MovementStatus
from apps.till.services import create_inscription_group_movement, get_cash_balance


def sync_group_inscriptions_status(group, status):
    group.fk_InscriptionGroup.update(status=status)


@transaction.atomic
def confirm_group_payment(group):
    group.payment_status = "C"
    group.save(update_fields=["payment_status", "modified"])
    sync_group_inscriptions_status(group, "C")
    create_inscription_group_movement(group)
    return group


@transaction.atomic
def reject_group_payment(group):
    if group.movements.exclude(status="VOID").exists():
        raise serializers.ValidationError(
            {
                "payment_status": (
                    "No se puede rechazar un grupo con movimiento de caja registrado."
                )
            }
        )

    group.payment_status = "R"
    group.save(update_fields=["payment_status", "modified"])
    sync_group_inscriptions_status(group, "R")
    return group


@transaction.atomic
def delete_inscription(inscription):
    """
    Elimina (soft-delete) una inscripcion.
    - Si el grupo esta PENDIENTE: solo soft-delete.
    - Si el grupo esta CONFIRMADO: valida saldo, anula Movement y recrea ajustado.
      Si es la ultima inscripcion, solo anula el Movement sin recrear.
    """
    group = inscription.group

    if group.payment_status == "C":
        balance = get_cash_balance(activity=group.activity)
        available = balance["cash_total"]

        if available - inscription.amount < 0:
            raise serializers.ValidationError(
                {
                    "inscripcion": (
                        f"No hay saldo suficiente en la caja para esta actividad. "
                        f"Saldo actual: {available}, monto a reversar: {inscription.amount}."
                    )
                }
            )

        original_movement = group.movements.filter(
            status=MovementStatus.POSTED
        ).first()

        if original_movement:
            new_amount = group.voucheramount - inscription.amount

            original_movement.status = MovementStatus.VOID
            original_movement.save(update_fields=["status", "modified"])

            if new_amount > 0:
                old_voucheramount = group.voucheramount
                group.voucheramount = new_amount
                group.save(update_fields=["voucheramount", "modified"])

                try:
                    create_inscription_group_movement(group)
                except Exception:
                    group.voucheramount = old_voucheramount
                    group.save(update_fields=["voucheramount", "modified"])
                    original_movement.status = MovementStatus.POSTED
                    original_movement.save(update_fields=["status", "modified"])
                    raise

    inscription.is_active = False
    inscription.save(update_fields=["is_active", "modified"])
