from django.apps import AppConfig


class UploadappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploadApp'
    def ready(self):
        import uploadApp.signals
