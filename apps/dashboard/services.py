from datetime import date

from django.db.models import (
    Avg,
    Case,
    CharField,
    Count,
    DecimalField,
    F,
    FloatField,
    Q,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Coalesce, ExtractDay, ExtractMonth

from apps.activity.models import Activity
from apps.inscription.models import Inscription, InscriptionGroup, Tarifa
from apps.person.models import Kind, Person
from apps.till.models import ConceptType, Movement, MovementStatus
from apps.till.services import get_cash_balance
from apps.user.models import Profile, User


def _build_birthday_date_filter(start_date, end_date):
    """Build Q filter for birthdays falling between two dates (month+day only)."""
    start_month = start_date.month
    start_day = start_date.day
    end_month = end_date.month
    end_day = end_date.day

    if start_month <= end_month:
        return (
            Q(birth_month=start_month, birth_day__gte=start_day)
            | Q(birth_month__gt=start_month, birth_month__lt=end_month)
            | Q(birth_month=end_month, birth_day__lte=end_day)
        )
    else:
        return (
            Q(birth_month=start_month, birth_day__gte=start_day)
            | Q(birth_month__gt=start_month)
            | Q(birth_month__lt=end_month)
            | Q(birth_month=end_month, birth_day__lte=end_day)
        )


def get_inscription_stats(activity):
    inscriptions = Inscription.objects.filter(
        group__activity=activity, is_active=True
    )

    stats = inscriptions.aggregate(
        total=Count("id"),
        attended_count=Count("id", filter=Q(checkinat__isnull=False)),
    )

    total = stats["total"] or 0
    attended = stats["attended_count"] or 0
    stats["attendance_rate"] = round(attended / total, 4) if total > 0 else 0

    by_status = list(
        inscriptions.values("status")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    status_map = dict(Inscription.STATUS_INSCRIPTION)
    stats["by_status"] = {
        status_map.get(item["status"], item["status"] or "SIN_ESTADO"): item["count"]
        for item in by_status
    }

    by_gender = list(
        inscriptions.values("person__gender")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    gender_map = dict(Person.GENDER_CHOICES)
    stats["by_gender"] = {
        gender_map.get(item["person__gender"], item["person__gender"] or "SIN_GENERO"): item["count"]
        for item in by_gender
    }

    by_kind_qs = (
        inscriptions.values("person__kind__id", "person__kind__description")
        .annotate(
            count=Count("id"),
            confirmed=Count("id", filter=Q(status="C")),
            attended=Count("id", filter=Q(checkinat__isnull=False)),
        )
        .order_by("-count")
    )
    stats["by_kind"] = [
        {
            "kind_id": item["person__kind__id"],
            "kind": item["person__kind__description"] or "SIN_TIPO",
            "count": item["count"],
            "confirmed": item["confirmed"],
            "attended": item["attended"],
        }
        for item in by_kind_qs
    ]

    return stats


def get_birthdays(activity):
    inscriptions = Inscription.objects.filter(
        group__activity=activity, is_active=True
    ).select_related("person", "person__church", "person__kind")

    person_ids = inscriptions.values_list("person_id", flat=True).distinct()

    annotated = Person.objects.filter(
        id__in=person_ids, birthdate__isnull=False
    ).annotate(
        birth_month=ExtractMonth("birthdate"),
        birth_day=ExtractDay("birthdate"),
    )

    date_filter = _build_birthday_date_filter(
        activity.start_date, activity.end_date
    )
    birthday_people = annotated.filter(date_filter)

    ins_map = {
        ins.person_id: ins
        for ins in inscriptions.filter(person__in=birthday_people)
    }
    status_map = dict(Inscription.STATUS_INSCRIPTION)

    result = []
    for person in birthday_people:
        ins = ins_map.get(person.id)
        today = date.today()
        age = (
            today.year
            - person.birthdate.year
            - (
                (today.month, today.day)
                < (person.birthdate.month, person.birthdate.day)
            )
        )
        result.append(
            {
                "person_id": person.id,
                "fullname": person.fullname,
                "birthdate": person.birthdate,
                "age_at_event": age,
                "gender": dict(Person.GENDER_CHOICES).get(
                    person.gender, person.gender or ""
                ),
                "church_name": person.church.description if person.church else None,
                "kind": person.kind.description if person.kind else None,
                "inscription_status": (
                    status_map.get(ins.status, ins.status)
                    if ins
                    else None
                ),
            }
        )

    return {"count": len(result), "people": result}


def get_financial_stats(activity):
    inscriptions = Inscription.objects.filter(
        group__activity=activity, is_active=True
    )
    agg = inscriptions.aggregate(
        total_expected=Coalesce(Sum("amount"), Value(0, output_field=DecimalField())),
        total_confirmed=Coalesce(
            Sum("amount", filter=Q(status="C")),
            Value(0, output_field=DecimalField()),
        ),
    )

    posted_totals = get_cash_balance(activity=activity)
    total_posted = posted_totals.get("total_incomes", 0)

    # Reduce inscriptions to unique groups for by_tarifa, by_payment_method
    unique_group_inscriptions = inscriptions.values(
        "group_id", "group__tarifa_id", "group__tarifa__description",
        "group__tarifa__price", "group__paymentmethod_id",
        "group__paymentmethod__description", "group__payment_status"
    ).distinct()

    # by_tarifa: count distinct groups + sum their inscriptions' amounts
    by_tarifa_raw = (
        inscriptions.values("group__tarifa__id")
        .annotate(
            tarifa_description=Coalesce(
                F("group__tarifa__description"), Value("Sin tarifa")
            ),
            tarifa_price=Coalesce(
                F("group__tarifa__price"), Value(0, output_field=DecimalField())
            ),
            inscription_count=Count("id"),
            total_amount=Coalesce(Sum("amount"), Value(0, output_field=DecimalField())),
            confirmed_amount=Coalesce(
                Sum("amount", filter=Q(status="C")),
                Value(0, output_field=DecimalField()),
            ),
        )
        .order_by("-total_amount")
    )
    by_tarifa = [
        {
            "tarifa_id": item["group__tarifa__id"],
            "description": item["tarifa_description"],
            "price": str(item["tarifa_price"]),
            "inscription_count": item["inscription_count"],
            "total_amount": str(item["total_amount"]),
            "confirmed_amount": str(item["confirmed_amount"]),
        }
        for item in by_tarifa_raw
    ]

    # by_payment_method from movements
    by_pm_raw = (
        Movement.objects.filter(
            activity=activity,
            status=MovementStatus.POSTED,
            concept__concept_type=ConceptType.INCOME,
        )
        .values("payment_method__id", "payment_method__description")
        .annotate(
            movement_count=Count("id"),
            total_amount=Coalesce(Sum("amount"), Value(0, output_field=DecimalField())),
        )
        .order_by("-total_amount")
    )
    by_payment_method = [
        {
            "payment_method_id": item["payment_method__id"],
            "description": item["payment_method__description"] or "Sin metodo",
            "movement_count": item["movement_count"],
            "total_amount": str(item["total_amount"]),
        }
        for item in by_pm_raw
    ]

    cash_balance = {
        "total_incomes": str(posted_totals.get("total_incomes", 0)),
        "total_expenses": str(posted_totals.get("total_expenses", 0)),
        "cash_total": str(posted_totals.get("cash_total", 0)),
        "movement_count": posted_totals.get("movement_count", 0),
    }

    total_expected = agg["total_expected"]
    total_confirmed = agg["total_confirmed"]

    return {
        "total_expected": str(total_expected),
        "total_confirmed": str(total_confirmed),
        "total_posted": str(total_posted),
        "pending_amount": str(total_expected - total_posted),
        "by_tarifa": by_tarifa,
        "by_payment_method": by_payment_method,
        "cash_balance": cash_balance,
    }


def get_churches_ranking(activity):
    inscriptions = Inscription.objects.filter(
        group__activity=activity, is_active=True
    )

    church_stats = list(
        inscriptions.values("person__church__id", "person__church__description")
        .annotate(
            total_inscriptions=Count("id"),
            confirmed=Count("id", filter=Q(status="C")),
            attended=Count("id", filter=Q(checkinat__isnull=False)),
            total_amount=Coalesce(
                Sum("amount"), Value(0, output_field=DecimalField())
            ),
            confirmed_amount=Coalesce(
                Sum("amount", filter=Q(status="C")),
                Value(0, output_field=DecimalField()),
            ),
        )
        .order_by("-total_inscriptions")
    )

    by_kind_raw = list(
        inscriptions.values(
            "person__church__id", "person__kind__id", "person__kind__description"
        )
        .annotate(count=Count("id"))
        .order_by("person__church__id", "-count")
    )

    kind_by_church = {}
    for item in by_kind_raw:
        cid = item["person__church__id"]
        if cid not in kind_by_church:
            kind_by_church[cid] = []
        kind_by_church[cid].append(
            {
                "kind_id": item["person__kind__id"],
                "kind": item["person__kind__description"] or "SIN_TIPO",
                "count": item["count"],
            }
        )

    result = []
    for church in church_stats:
        cid = church["person__church__id"]
        result.append(
            {
                "church_id": cid,
                "church_name": church["person__church__description"] or "Sin iglesia",
                "total_inscriptions": church["total_inscriptions"],
                "confirmed": church["confirmed"],
                "attended": church["attended"],
                "total_amount": str(church["total_amount"]),
                "confirmed_amount": str(church["confirmed_amount"]),
                "by_kind": kind_by_church.get(cid, []),
            }
        )

    return result


def get_groups_stats(activity):
    groups = InscriptionGroup.objects.filter(activity=activity)
    agg = groups.aggregate(
        total=Count("id"),
    )

    by_status = list(
        groups.values("payment_status")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    status_map = dict(InscriptionGroup.PAYMENT_STATUS)
    agg["by_payment_status"] = {
        status_map.get(item["payment_status"], item["payment_status"]): item["count"]
        for item in by_status
    }

    group_sizes = (
        Inscription.objects.filter(group__activity=activity, is_active=True)
        .values("group_id")
        .annotate(size=Count("id"))
        .aggregate(avg=Coalesce(Avg("size"), Value(0, output_field=FloatField())))
    )
    agg["average_size"] = round(group_sizes["avg"], 2) if group_sizes["avg"] else 0

    return agg


def get_users_stats(activity):
    users = User.objects.filter(activity=activity)
    total = users.count()

    by_profile = list(
        users.values("profile__description")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    by_profile_map = {
        item["profile__description"] or "SIN_PERFIL": item["count"]
        for item in by_profile
    }

    return {"total": total, "by_profile": by_profile_map}


def get_activity_dashboard(activity):
    return {
        "activity": {
            "id": activity.id,
            "title": activity.title,
            "shortname": activity.shortname,
            "start_date": activity.start_date,
            "end_date": activity.end_date,
            "is_active": activity.is_active,
            "is_ended": activity.is_ended,
            "settings": activity.settings,
        },
        "inscriptions": get_inscription_stats(activity),
        "birthdays": get_birthdays(activity),
        "financial": get_financial_stats(activity),
        "churches_ranking": get_churches_ranking(activity),
        "groups": get_groups_stats(activity),
        "users": get_users_stats(activity),
    }
