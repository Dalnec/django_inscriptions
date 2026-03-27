from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inscription", "0003_initial"),
        ("till", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="movement",
            name="inscription_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="movements",
                to="inscription.inscriptiongroup",
            ),
        ),
    ]
