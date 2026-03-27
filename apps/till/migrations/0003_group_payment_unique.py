from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("till", "0002_movement_inscription_group"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="movement",
            constraint=models.UniqueConstraint(
                condition=models.Q(inscription_group__isnull=False),
                fields=("inscription_group",),
                name="till_movement_one_group_payment",
            ),
        ),
    ]
