from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.activity.models import Activity
from apps.inscription.models import Inscription, InscriptionGroup, PaymentMethod
from apps.person.models import DocumentType, Person
from apps.till.models import Concept, ConceptType, Movement, MovementStatus
from apps.user.models import User


class TillModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="TESTUSER01", email="test01@mail.com")
        self.activity = Activity.objects.create(
            title="Evento Caja",
            start_date="2026-03-20 09:00:00",
            end_date="2026-03-20 18:00:00",
        )
        self.another_activity = Activity.objects.create(
            title="Evento Alterno",
            start_date="2026-03-21 09:00:00",
            end_date="2026-03-21 18:00:00",
        )
        self.income_concept = Concept.objects.create(
            description="INSCRIPCION", concept_type=ConceptType.INCOME
        )
        self.expense_concept = Concept.objects.create(
            description="MATERIAL", concept_type=ConceptType.EXPENSE
        )

    def _build_inscription(self):
        document_type = DocumentType.objects.create(description="DNI", active=True)
        person = Person.objects.create(
            doc_num="12345678",
            names="Carlos",
            lastnames="Perez",
            status=True,
            documenttype=document_type,
            user=self.user,
        )
        group = InscriptionGroup.objects.create(
            vouchergroup="G0001",
            voucheramount=Decimal("100.00"),
            activity=self.activity,
            user=self.user,
        )
        return Inscription.objects.create(
            amount=Decimal("100.00"),
            group=group,
            person=person,
            status="P",
        )

    def test_signed_amount_uses_concept_type(self):
        income = Movement.objects.create(
            activity=self.activity,
            concept=self.income_concept,
            amount=Decimal("80.00"),
            status=MovementStatus.DRAFT,
        )
        expense = Movement.objects.create(
            activity=self.activity,
            concept=self.expense_concept,
            amount=Decimal("35.50"),
            status=MovementStatus.DRAFT,
        )

        self.assertEqual(income.signed_amount, Decimal("80.00"))
        self.assertEqual(expense.signed_amount, Decimal("-35.50"))

    def test_amount_must_be_positive(self):
        with self.assertRaises(ValidationError):
            Movement.objects.create(
                activity=self.activity,
                concept=self.income_concept,
                amount=Decimal("0.00"),
            )

    def test_posted_movement_cannot_change_locked_fields(self):
        movement = Movement.objects.create(
            activity=self.activity,
            concept=self.income_concept,
            amount=Decimal("90.00"),
            status=MovementStatus.POSTED,
        )

        movement.amount = Decimal("91.00")
        with self.assertRaises(ValidationError):
            movement.save()

    def test_reversal_requires_void_status(self):
        origin = Movement.objects.create(
            activity=self.activity,
            concept=self.income_concept,
            amount=Decimal("90.00"),
            status=MovementStatus.POSTED,
        )
        reversal = Movement(
            activity=self.activity,
            concept=self.expense_concept,
            amount=Decimal("90.00"),
            status=MovementStatus.DRAFT,
            reversal_of=origin,
        )

        with self.assertRaises(ValidationError):
            reversal.save()

    def test_only_one_reversal_per_movement(self):
        origin = Movement.objects.create(
            activity=self.activity,
            concept=self.income_concept,
            amount=Decimal("120.00"),
            status=MovementStatus.POSTED,
        )
        Movement.objects.create(
            activity=self.activity,
            concept=self.expense_concept,
            amount=Decimal("120.00"),
            status=MovementStatus.VOID,
            reversal_of=origin,
        )

        with self.assertRaises(ValidationError):
            Movement.objects.create(
                activity=self.activity,
                concept=self.expense_concept,
                amount=Decimal("120.00"),
                status=MovementStatus.VOID,
                reversal_of=origin,
            )

    def test_inscription_activity_must_match_movement_activity(self):
        inscription = self._build_inscription()
        movement = Movement(
            activity=self.another_activity,
            concept=self.income_concept,
            amount=Decimal("100.00"),
            inscription=inscription,
        )

        with self.assertRaises(ValidationError):
            movement.save()

    def test_inscription_group_activity_must_match_movement_activity(self):
        group = InscriptionGroup.objects.create(
            vouchergroup="G0002",
            voucheramount=Decimal("150.00"),
            activity=self.activity,
            user=self.user,
        )
        movement = Movement(
            activity=self.another_activity,
            concept=self.income_concept,
            amount=Decimal("150.00"),
            inscription_group=group,
        )

        with self.assertRaises(ValidationError):
            movement.save()


class TillApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="APIUSER001", email="api001@mail.com")
        self.activity = Activity.objects.create(
            title="Evento API Caja",
            start_date="2026-03-25 09:00:00",
            end_date="2026-03-25 18:00:00",
            settings={"inscription": {"send_email": False, "emails": []}},
        )
        self.concept = Concept.objects.create(
            description="INSCRIPCION",
            concept_type=ConceptType.INCOME,
        )
        self.expense_concept = Concept.objects.create(
            description="GASTO API",
            concept_type=ConceptType.EXPENSE,
        )
        self.cash_payment_method = PaymentMethod.objects.create(
            description="EFECTIVO",
            active=True,
        )
        self.transfer_payment_method = PaymentMethod.objects.create(
            description="TRANSFERENCIA",
            active=True,
        )
        self.tarifa = self._create_tarifa()

    def _create_tarifa(self):
        from apps.inscription.models import Tarifa

        return Tarifa.objects.create(
            description="GENERAL",
            price=Decimal("50.00"),
            active=True,
            selected=True,
        )

    def _create_inscription_for_activity(self, activity, doc_num):
        document_type = DocumentType.objects.create(
            description=f"DOC-{doc_num}",
            active=True,
        )
        person = Person.objects.create(
            doc_num=doc_num,
            names="Persona",
            lastnames="Inscripcion",
            status=True,
            documenttype=document_type,
            user=self.user,
        )
        group = InscriptionGroup.objects.create(
            vouchergroup=f"G{doc_num}",
            voucheramount=Decimal("30.00"),
            activity=activity,
            user=self.user,
        )
        return Inscription.objects.create(
            amount=Decimal("30.00"),
            group=group,
            person=person,
            status="P",
        )

    def _build_register_group_payload(self, voucheramount="100.00"):
        document_type = DocumentType.objects.create(
            description=f"DOC-PAYLOAD-{DocumentType.objects.count() + 1}",
            active=True,
        )
        return {
            "activity": self.activity.id,
            "voucheramount": voucheramount,
            "paymentmethod": self.cash_payment_method.id,
            "tarifa": self.tarifa.id,
            "user": self.user.id,
            "people": [
                {
                    "doc_num": "77112233",
                    "names": "Ana",
                    "lastnames": "Lopez",
                    "status": True,
                    "documenttype": document_type.id,
                },
                {
                    "doc_num": "77112234",
                    "names": "Luis",
                    "lastnames": "Diaz",
                    "status": True,
                    "documenttype": document_type.id,
                },
            ],
        }

    def _register_group(self, voucheramount="100.00"):
        response = self.client.post(
            reverse("inscription-group-register-group"),
            self._build_register_group_payload(voucheramount=voucheramount),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return InscriptionGroup.objects.get(pk=response.data["group_id"])

    def test_create_and_list_concepts(self):
        create_url = reverse("till-concept-list")
        payload = {
            "description": "DONACION",
            "concept_type": ConceptType.INCOME,
            "is_active": True,
            "is_internal": False,
        }
        response = self.client.post(create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        list_response = self.client.get(create_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(list_response.data["count"], 2)

    def test_create_movement_and_filter_by_activity(self):
        url = reverse("till-movement-list")
        payload = {
            "movement_at": "2026-03-25 10:00:00",
            "description": "Ingreso por caja",
            "reference": "REF-001",
            "amount": "75.00",
            "status": "POSTED",
            "concept": self.concept.id,
            "activity": self.activity.id,
            "user": self.user.id,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["signed_amount"], "75.00")

        list_response = self.client.get(url, {"activity": self.activity.id})
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 1)
        self.assertIn("meta", list_response.data)
        self.assertEqual(list_response.data["meta"]["total_incomes"], "75.00")
        self.assertEqual(list_response.data["meta"]["total_expenses"], "0")
        self.assertEqual(list_response.data["meta"]["total_inscriptions"], "0")
        self.assertEqual(list_response.data["meta"]["cash_total"], "75.00")

    def test_movement_create_rejects_activity_mismatch_with_inscription(self):
        document_type = DocumentType.objects.create(description="CE", active=True)
        person = Person.objects.create(
            doc_num="99887766",
            names="Mariela",
            lastnames="Lopez",
            status=True,
            documenttype=document_type,
            user=self.user,
        )
        group = InscriptionGroup.objects.create(
            vouchergroup="GAPI001",
            voucheramount=Decimal("60.00"),
            activity=self.activity,
            user=self.user,
        )
        inscription = Inscription.objects.create(
            amount=Decimal("60.00"),
            group=group,
            person=person,
            status="P",
        )
        another_activity = Activity.objects.create(
            title="Evento API Distinto",
            start_date="2026-03-26 09:00:00",
            end_date="2026-03-26 18:00:00",
        )

        url = reverse("till-movement-list")
        payload = {
            "movement_at": "2026-03-25 11:00:00",
            "description": "Ingreso inconsistente",
            "reference": "REF-ERR",
            "amount": "60.00",
            "status": "DRAFT",
            "concept": self.concept.id,
            "activity": another_activity.id,
            "inscription": inscription.id,
            "user": self.user.id,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("activity", response.data)

    def test_register_group_starts_pending_without_cash_movement(self):
        group = self._register_group(voucheramount="100.00")

        self.assertEqual(group.fk_InscriptionGroup.count(), 2)
        self.assertEqual(group.payment_status, "P")
        self.assertEqual(Movement.objects.filter(inscription_group=group).count(), 0)

    def test_confirm_payment_creates_posted_cash_movement(self):
        group = self._register_group(voucheramount="100.00")
        url = reverse("inscription-group-confirm-payment", args=[group.id])

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group.refresh_from_db()
        movement = Movement.objects.get(inscription_group=group)
        self.assertEqual(group.payment_status, "C")
        self.assertEqual(movement.amount, Decimal("100.00"))
        self.assertEqual(movement.status, MovementStatus.POSTED)
        self.assertEqual(movement.reference, group.vouchergroup)
        self.assertEqual(movement.concept_id, self.concept.id)
        self.assertEqual(movement.payment_method_id, self.cash_payment_method.id)
        self.assertEqual(movement.user_id, self.user.id)
        self.assertEqual(
            set(group.fk_InscriptionGroup.values_list("status", flat=True)),
            {"C"},
        )

    def test_confirm_payment_rolls_back_when_cash_concept_is_missing(self):
        group = self._register_group(voucheramount="80.00")
        self.concept.delete()
        url = reverse("inscription-group-confirm-payment", args=[group.id])

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        group.refresh_from_db()
        self.assertEqual(group.payment_status, "P")
        self.assertEqual(Movement.objects.count(), 0)

    def test_confirm_payment_is_idempotent_for_group(self):
        group = self._register_group(voucheramount="90.00")
        url = reverse("inscription-group-confirm-payment", args=[group.id])

        first_response = self.client.post(url, {}, format="json")
        second_response = self.client.post(url, {}, format="json")

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movement.objects.filter(inscription_group=group).count(), 1)

    def test_reject_payment_updates_group_without_cash_movement(self):
        group = self._register_group(voucheramount="70.00")
        url = reverse("inscription-group-reject-payment", args=[group.id])

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group.refresh_from_db()
        self.assertEqual(group.payment_status, "R")
        self.assertEqual(Movement.objects.filter(inscription_group=group).count(), 0)
        self.assertEqual(
            set(group.fk_InscriptionGroup.values_list("status", flat=True)),
            {"R"},
        )

    def test_reject_payment_fails_when_cash_movement_exists(self):
        group = self._register_group(voucheramount="70.00")
        self.client.post(
            reverse("inscription-group-confirm-payment", args=[group.id]),
            {},
            format="json",
        )
        url = reverse("inscription-group-reject-payment", args=[group.id])

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        group.refresh_from_db()
        self.assertEqual(group.payment_status, "C")
        self.assertEqual(Movement.objects.filter(inscription_group=group).count(), 1)

    def test_updating_checkin_does_not_change_group_payment_status(self):
        group = self._register_group(voucheramount="70.00")
        inscription = group.fk_InscriptionGroup.first()
        url = reverse("inscription-detail", args=[inscription.id])

        response = self.client.put(
            url,
            {
                "amount": str(inscription.amount),
                "observations": inscription.observations,
                "checkinat": "2026-03-25T12:30:00",
                "status": "R",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        inscription.refresh_from_db()
        group.refresh_from_db()
        self.assertIsNotNone(inscription.checkinat)
        self.assertEqual(inscription.status, "P")
        self.assertEqual(group.payment_status, "P")

    def test_summary_returns_totals_and_breakdown(self):
        Movement.objects.create(
            activity=self.activity,
            concept=self.concept,
            amount=Decimal("150.00"),
            status=MovementStatus.POSTED,
            payment_method=self.cash_payment_method,
            user=self.user,
        )
        Movement.objects.create(
            activity=self.activity,
            concept=self.concept,
            amount=Decimal("70.00"),
            status=MovementStatus.POSTED,
            payment_method=self.transfer_payment_method,
            user=self.user,
        )
        Movement.objects.create(
            activity=self.activity,
            concept=self.expense_concept,
            amount=Decimal("40.00"),
            status=MovementStatus.POSTED,
            payment_method=self.cash_payment_method,
            user=self.user,
        )

        url = reverse("till-movement-summary")
        response = self.client.get(url, {"activity": self.activity.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["totals"]["total_incomes"], "220.00")
        self.assertEqual(response.data["totals"]["total_expenses"], "40.00")
        self.assertEqual(response.data["totals"]["cash_total"], "180.00")
        self.assertEqual(response.data["totals"]["total_inscriptions"], "0")
        self.assertEqual(response.data["totals"]["movement_count"], 3)
        self.assertEqual(len(response.data["by_payment_method"]), 2)

    def test_list_meta_uses_filtered_queryset_and_counts_inscriptions(self):
        inscription = self._create_inscription_for_activity(self.activity, "44556677")
        other_activity = Activity.objects.create(
            title="Evento Otro",
            start_date="2026-03-27 09:00:00",
            end_date="2026-03-27 18:00:00",
        )

        Movement.objects.create(
            activity=self.activity,
            concept=self.concept,
            amount=Decimal("100.00"),
            status=MovementStatus.POSTED,
            inscription=inscription,
            payment_method=self.cash_payment_method,
            user=self.user,
        )
        Movement.objects.create(
            activity=self.activity,
            concept=self.expense_concept,
            amount=Decimal("30.00"),
            status=MovementStatus.POSTED,
            payment_method=self.cash_payment_method,
            user=self.user,
        )
        Movement.objects.create(
            activity=other_activity,
            concept=self.concept,
            amount=Decimal("500.00"),
            status=MovementStatus.POSTED,
            payment_method=self.transfer_payment_method,
            user=self.user,
        )

        url = reverse("till-movement-list")
        response = self.client.get(url, {"activity": self.activity.id, "page_size": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["meta"]["total_incomes"], "100.00")
        self.assertEqual(response.data["meta"]["total_expenses"], "30.00")
        self.assertEqual(response.data["meta"]["total_inscriptions"], "100.00")
        self.assertEqual(response.data["meta"]["cash_total"], "70.00")
        self.assertEqual(response.data["meta"]["movement_count"], 2)

    def test_list_meta_counts_group_movements_as_inscriptions_and_filters_them(self):
        group = InscriptionGroup.objects.create(
            vouchergroup="GAPI999",
            voucheramount=Decimal("120.00"),
            activity=self.activity,
            user=self.user,
            paymentmethod=self.cash_payment_method,
            tarifa=self.tarifa,
        )
        Movement.objects.create(
            activity=self.activity,
            concept=self.concept,
            amount=Decimal("120.00"),
            status=MovementStatus.POSTED,
            inscription_group=group,
            payment_method=self.cash_payment_method,
            user=self.user,
        )

        url = reverse("till-movement-list")
        response = self.client.get(
            url,
            {"activity": self.activity.id, "inscription_group": group.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["inscription_group"], group.id)
        self.assertEqual(response.data["meta"]["total_inscriptions"], "120.00")
