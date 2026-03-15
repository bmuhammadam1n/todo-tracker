# tasks/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Task
from analytics.utils import update_daily_progress

@receiver(post_save, sender=Task)
def task_saved_handler(sender, instance, created, **kwargs):
    """Update daily progress when a task is created or updated"""
    # Update progress for the date the task was created
    update_daily_progress(instance.user, instance.created_at.date())
    
    # If task has a due date, also update that day's progress
    if instance.due_date:
        update_daily_progress(instance.user, instance.due_date)
    
    # Always update today's progress too
    update_daily_progress(instance.user, timezone.now().date())

@receiver(post_delete, sender=Task)
def task_deleted_handler(sender, instance, **kwargs):
    """Update daily progress when a task is deleted"""
    # Update progress for the date the task was created
    update_daily_progress(instance.user, instance.created_at.date())
    
    # If task had a due date, also update that day's progress
    if instance.due_date:
        update_daily_progress(instance.user, instance.due_date)
    
    # Always update today's progress too
    update_daily_progress(instance.user, timezone.now().date())