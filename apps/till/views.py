from django.db.models import Case, Count, DecimalField, F, Sum, Value, When
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import (
    ConceptFilter,
    ConceptPagination,
    MovementFilter,
    MovementPagination,
)
from .models import Concept, Movement
from .serializers import ConceptSerializer, MovementSerializer


@extend_schema(tags=["TillConcept"])
class ConceptViewSet(viewsets.GenericViewSet):
    serializer_class = ConceptSerializer
    queryset = Concept.objects.all().order_by("description")
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConceptFilter
    pagination_class = ConceptPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["TillMovement"])
class MovementViewSet(viewsets.GenericViewSet):
    serializer_class = MovementSerializer
    queryset = Movement.objects.select_related(
        "activity", "concept", "inscription", "payment_method", "user", "reversal_of"
    ).order_by("-movement_at", "-id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovementFilter
    pagination_class = MovementPagination

    def _calculate_totals(self, queryset):
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
            total_inscriptions=Coalesce(
                Sum(
                    Case(
                        When(inscription__isnull=False, then=F("amount")),
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

    def _serialize_totals(self, totals):
        return {
            "total_incomes": str(totals["total_incomes"]),
            "total_expenses": str(totals["total_expenses"]),
            "total_inscriptions": str(totals["total_inscriptions"]),
            "cash_total": str(totals["cash_total"]),
            "movement_count": totals["movement_count"],
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        meta = self._serialize_totals(self._calculate_totals(queryset))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["meta"] = meta
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"results": serializer.data, "meta": meta}, status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        totals = self._calculate_totals(queryset)

        by_payment_method = list(
            queryset.values("payment_method_id", "payment_method__description")
            .annotate(
                incomes=Coalesce(
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
                expenses=Coalesce(
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
            .order_by("payment_method__description")
        )

        response_data = {
            "filters": request.query_params.dict(),
            "totals": self._serialize_totals(totals),
            "by_payment_method": [
                {
                    "payment_method_id": item["payment_method_id"],
                    "payment_method": item["payment_method__description"],
                    "incomes": str(item["incomes"]),
                    "expenses": str(item["expenses"]),
                    "net_balance": str(item["incomes"] - item["expenses"]),
                    "movement_count": item["movement_count"],
                }
                for item in by_payment_method
            ],
        }
        return Response(response_data, status=status.HTTP_200_OK)

