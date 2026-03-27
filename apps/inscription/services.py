from django.db import transaction
from rest_framework import serializers

from apps.till.services import create_inscription_group_movement


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
