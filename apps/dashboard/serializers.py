from rest_framework import serializers


class ActivitySummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    shortname = serializers.CharField(allow_null=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    is_ended = serializers.BooleanField()
    settings = serializers.JSONField(allow_null=True)


class ByStatusSerializer(serializers.Serializer):
    PENDIENTE = serializers.IntegerField(default=0)
    CONFIRMADO = serializers.IntegerField(default=0)
    RECHAZADO = serializers.IntegerField(default=0)
    ERROR = serializers.IntegerField(default=0)


class ByKindItemSerializer(serializers.Serializer):
    kind_id = serializers.IntegerField(allow_null=True)
    kind = serializers.CharField()
    count = serializers.IntegerField()
    confirmed = serializers.IntegerField()
    attended = serializers.IntegerField()


class InscriptionStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    by_status = serializers.DictField(child=serializers.IntegerField())
    attended_count = serializers.IntegerField()
    attendance_rate = serializers.FloatField()
    by_gender = serializers.DictField(child=serializers.IntegerField())
    by_kind = ByKindItemSerializer(many=True)


class BirthdayPersonSerializer(serializers.Serializer):
    person_id = serializers.IntegerField()
    fullname = serializers.CharField()
    birthdate = serializers.DateField()
    age_at_event = serializers.IntegerField()
    gender = serializers.CharField(allow_blank=True)
    church_name = serializers.CharField(allow_null=True)
    kind = serializers.CharField(allow_null=True)
    inscription_status = serializers.CharField(allow_null=True)


class BirthdaysSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    people = BirthdayPersonSerializer(many=True)


class TarifaBreakdownSerializer(serializers.Serializer):
    tarifa_id = serializers.IntegerField(allow_null=True)
    description = serializers.CharField()
    price = serializers.CharField()
    inscription_count = serializers.IntegerField()
    total_amount = serializers.CharField()
    confirmed_amount = serializers.CharField()


class PaymentMethodBreakdownSerializer(serializers.Serializer):
    payment_method_id = serializers.IntegerField(allow_null=True)
    description = serializers.CharField()
    movement_count = serializers.IntegerField()
    total_amount = serializers.CharField()


class CashBalanceSerializer(serializers.Serializer):
    total_incomes = serializers.CharField()
    total_expenses = serializers.CharField()
    cash_total = serializers.CharField()
    movement_count = serializers.IntegerField()


class FinancialStatsSerializer(serializers.Serializer):
    total_expected = serializers.CharField()
    total_confirmed = serializers.CharField()
    total_posted = serializers.CharField()
    pending_amount = serializers.CharField()
    by_tarifa = TarifaBreakdownSerializer(many=True)
    by_payment_method = PaymentMethodBreakdownSerializer(many=True)
    cash_balance = CashBalanceSerializer()


class ChurchKindBreakdownSerializer(serializers.Serializer):
    kind_id = serializers.IntegerField(allow_null=True)
    kind = serializers.CharField()
    count = serializers.IntegerField()


class ChurchRankingItemSerializer(serializers.Serializer):
    church_id = serializers.IntegerField(allow_null=True)
    church_name = serializers.CharField()
    total_inscriptions = serializers.IntegerField()
    confirmed = serializers.IntegerField()
    attended = serializers.IntegerField()
    total_amount = serializers.CharField()
    confirmed_amount = serializers.CharField()
    by_kind = ChurchKindBreakdownSerializer(many=True)


class GroupsStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    by_payment_status = serializers.DictField(child=serializers.IntegerField())
    average_size = serializers.FloatField()


class UsersStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    by_profile = serializers.DictField(child=serializers.IntegerField())


class DashboardSerializer(serializers.Serializer):
    activity = ActivitySummarySerializer()
    inscriptions = InscriptionStatsSerializer()
    birthdays = BirthdaysSerializer()
    financial = FinancialStatsSerializer()
    churches_ranking = ChurchRankingItemSerializer(many=True)
    groups = GroupsStatsSerializer()
    users = UsersStatsSerializer()
