class ExternalRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'kenani':
            return 'externa'
        return None

    def db_for_write(self, model, **hints):
        return None  # Solo lectura

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return False  # No hacer migraciones en externa
