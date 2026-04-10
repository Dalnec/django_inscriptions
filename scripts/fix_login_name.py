from django.db import transaction
from django.db.models import Q
from apps.user.models import User
from apps.activity.models import Activity

def migrate_users_to_new_format():
    users = User.objects.filter(Q(login_name="")|Q(login_name__isnull=True),is_superuser=False)
    activity = Activity.objects.all().last()
    users.update(activity=activity)
    count = 0
    print(f"Iniciando actualización de {users.count()} usuarios...")
    with transaction.atomic():
        for user in users:
            if not user.activity:
                print(f"Saltando usuario ID {user.id}: No tiene actividad.")
                continue
            original_username = user.username
            user.login_name = original_username
            # Forzamos la lógica del modelo
            shortname = user.activity.shortname.upper()
            user.username = f"{shortname}_{original_username}".upper()
            try:
                user.save()
                count += 1
                print(f"Actualizado: {original_username} -> {user.username}")
            except Exception as e:
                print(f"Error en {original_username}: {e}")
    print(f"Terminado. {count} usuarios actualizados.")

# Ejecución inmediata
migrate_users_to_new_format()