from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class ConceptType(models.TextChoices):
    INCOME = "I", "INGRESO"
    EXPENSE = "E", "EGRESO"


class Concept(TimeStampedModel):
    description = models.CharField("Descripcion", max_length=150)
    concept_type = models.CharField(
        "Tipo de Concepto",
        max_length=1,
        choices=ConceptType.choices,
        default=ConceptType.INCOME,
    )
    is_active = models.BooleanField(default=True)
    is_internal = models.BooleanField(default=False)
    activity = models.ForeignKey(
        "activity.Activity",
        on_delete=models.PROTECT,
        related_name="concept_activities",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Concepto"
        verbose_name_plural = "Conceptos"
        db_table = "Concept"
        constraints = [
            models.UniqueConstraint(
                fields=["description", "activity"],
                name="unique_concept_activity",
                nulls_distinct=False,
            )
        ]

    def __str__(self):
        return self.description


class MovementStatus(models.TextChoices):
    DRAFT = "DRAFT", "BORRADOR"
    POSTED = "POSTED", "CONTABILIZADO"
    VOID = "VOID", "ANULADO"


class Movement(TimeStampedModel):
    movement_at = models.DateTimeField("Fecha", default=timezone.now, db_index=True)
    description = models.CharField("Descripcion", max_length=250, null=True, blank=True)
    reference = models.CharField(
        "Documento Referencia", max_length=100, null=True, blank=True
    )
    amount = models.DecimalField(
        "Monto",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    status = models.CharField(
        "Estado",
        max_length=10,
        choices=MovementStatus.choices,
        default=MovementStatus.DRAFT,
        db_index=True,
    )
    concept = models.ForeignKey(
        Concept, on_delete=models.PROTECT, related_name="movements"
    )
    payment_method = models.ForeignKey(
        "inscription.PaymentMethod",
        on_delete=models.SET_NULL,
        verbose_name="Metodo de Pago",
        related_name="movements",
        null=True,
        blank=True,
    )
    inscription = models.ForeignKey(
        "inscription.Inscription",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements",
    )
    inscription_group = models.ForeignKey(
        "inscription.InscriptionGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements",
    )
    user = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements",
    )
    activity = models.ForeignKey(
        "activity.Activity",
        on_delete=models.PROTECT,
        related_name="movements",
    )
    reversal_of = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reversed_by",
    )

    class Meta:
        verbose_name = "Movimiento de Caja"
        verbose_name_plural = "Movimientos de Caja"
        db_table = "Movements"
        indexes = [
            models.Index(fields=["activity", "movement_at"], name="till_act_date_idx"),
            models.Index(fields=["concept", "movement_at"], name="till_con_date_idx"),
            models.Index(fields=["status", "movement_at"], name="till_sta_date_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=0), name="till_movement_amount_gt_zero"
            ),
            models.CheckConstraint(
                check=~models.Q(id=models.F("reversal_of")),
                name="till_movement_not_self_reverse",
            ),
            models.UniqueConstraint(
                fields=["reversal_of"],
                condition=models.Q(reversal_of__isnull=False),
                name="till_movement_one_reversal",
            ),
            models.UniqueConstraint(
                fields=["inscription_group"],
                condition=models.Q(inscription_group__isnull=False),
                name="till_movement_one_group_payment",
            ),
        ]

    def __str__(self):
        return f"{self.id} - {self.get_status_display()} - {self.amount}"

    @property
    def signed_amount(self):
        if self.concept.concept_type == ConceptType.EXPENSE:
            return -self.amount
        return self.amount

    def clean(self):
        errors = {}
        if self.inscription_id:
            inscription_activity_id = self.inscription.group.activity_id
            if inscription_activity_id != self.activity_id:
                errors["activity"] = (
                    "La actividad del movimiento debe coincidir con la actividad de la "
                    "inscripcion."
                )
        if self.inscription_group_id:
            inscription_group_activity_id = self.inscription_group.activity_id
            if inscription_group_activity_id != self.activity_id:
                errors["activity"] = (
                    "La actividad del movimiento debe coincidir con la actividad del "
                    "grupo de inscripcion."
                )
        if self.reversal_of_id:
            if self.status != MovementStatus.VOID:
                errors["status"] = "Un movimiento reverso debe estar en estado ANULADO."
            if self.reversal_of.status == MovementStatus.VOID:
                errors["reversal_of"] = "No se puede revertir un movimiento ya anulado."
        if self.pk:
            original = Movement.objects.filter(pk=self.pk).first()
            if original and original.status == MovementStatus.POSTED:
                locked_changed = (
                    original.amount != self.amount
                    or original.concept_id != self.concept_id
                    or original.activity_id != self.activity_id
                )
                if locked_changed:
                    errors["status"] = (
                        "No se puede modificar monto, concepto o actividad "
                        "de un movimiento contabilizado."
                    )
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def available_amount(self):
        from .services import get_cash_balance
        return get_cash_balance(activity=self.activity)
