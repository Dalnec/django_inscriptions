import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")
django.setup()

from apps.till.models import Concept, ConceptType
from apps.activity.models import Activity
from django.db import IntegrityError
from django.utils import timezone

def run_test():
    print("Starting uniqueness tests...")
    
    # Setup: Get or create two activities
    act1, _ = Activity.objects.get_or_create(
        shortname="TEST_ACT_1",
        defaults={
            "title": "Test Activity 1",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(days=1)
        }
    )
    act2, _ = Activity.objects.get_or_create(
        shortname="TEST_ACT_2",
        defaults={
            "title": "Test Activity 2",
            "start_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(days=1)
        }
    )

    concept_name = "Concepto de Prueba"

    # Cleanup any existing concepts with this name
    Concept.objects.filter(description=concept_name).delete()

    # 1. Test: Same name, different activities (Should PASS)
    try:
        c1 = Concept.objects.create(description=concept_name, activity=act1)
        c2 = Concept.objects.create(description=concept_name, activity=act2)
        print("Success: Created same concept name in different activities.")
    except Exception as e:
        print(f"Fail: Could not create same concept name in different activities: {e}")

    # 2. Test: Same name, same activity (Should FAIL)
    try:
        Concept.objects.create(description=concept_name, activity=act1)
        print("Fail: Created duplicate concept name in the same activity (should have failed)!")
    except IntegrityError:
        print("Success: Caught IntegrityError for duplicate name in same activity.")
    except Exception as e:
        print(f"Error: Unexpected exception for duplicate name in same activity: {e}")

    # 3. Test: Same name, activity is NULL (Should FAIL if second one created)
    concept_name_null = "Global Concept"
    Concept.objects.filter(description=concept_name_null).delete()
    
    try:
        Concept.objects.create(description=concept_name_null, activity=None)
        print("Created first global concept.")
        Concept.objects.create(description=concept_name_null, activity=None)
        print("Fail: Created second global concept (should have failed)!")
    except IntegrityError:
        print("Success: Caught IntegrityError for duplicate global concept name.")
    except Exception as e:
        print(f"Error: Unexpected exception for duplicate global concept name: {e}")

    # Cleanup
    Concept.objects.filter(description__in=[concept_name, concept_name_null]).delete()
    act1.delete()
    act2.delete()
    print("Cleanup done.")

if __name__ == "__main__":
    run_test()
