from django.db import migrations, models


def backfill_group_payment_status(apps, schema_editor):
    Inscription = apps.get_model("inscription", "Inscription")
    InscriptionGroup = apps.get_model("inscription", "InscriptionGroup")

    for inscription in Inscription.objects.filter(status="A"):
        if inscription.checkinat is None:
            inscription.checkinat = inscription.modified or inscription.created
        inscription.status = "C"
        inscription.save(update_fields=["status", "checkinat", "modified"])

    for group in InscriptionGroup.objects.all():
        statuses = list(
            Inscription.objects.filter(group_id=group.id)
            .exclude(status__isnull=True)
            .values_list("status", flat=True)
            .distinct()
        )
        if len(statuses) == 1 and statuses[0] in {"P", "C", "R", "E"}:
            group.payment_status = statuses[0]
        elif len(statuses) == 0:
            group.payment_status = "P"
        else:
            group.payment_status = "E"
        group.save(update_fields=["payment_status", "modified"])


class Migration(migrations.Migration):

    dependencies = [
        ("inscription", "0003_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="inscriptiongroup",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("P", "PENDIENTE"),
                    ("C", "CONFIRMADO"),
                    ("R", "RECHAZADO"),
                    ("E", "ERROR"),
                ],
                default="P",
                max_length=1,
            ),
        ),
        migrations.RunPython(
            backfill_group_payment_status,
            migrations.RunPython.noop,
        ),
    ]
