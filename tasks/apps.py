# tasks/apps.py
from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    
    def ready(self):
        # Import signals to register them
        import tasks.signals