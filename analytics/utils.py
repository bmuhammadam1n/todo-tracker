# analytics/utils.py
from django.utils import timezone
from .models import DailyProgress
from tasks.models import Task

def get_or_create_daily_progress(user, date=None):
    """Get or create a DailyProgress record for a user on a specific date"""
    if date is None:
        date = timezone.now().date()
    
    progress, created = DailyProgress.objects.get_or_create(
        user=user,
        date=date,
        defaults={'total_tasks': 0, 'completed_tasks': 0}
    )
    return progress

def update_daily_progress(user, date=None):
    """Recalculate and update progress for a user on a specific date"""
    if date is None:
        date = timezone.now().date()
    
    progress = get_or_create_daily_progress(user, date)
    
    # Get all tasks for this user on this date (created today OR due today)
    tasks_today = Task.objects.filter(
        user=user,
        created_at__date=date  # Tasks created today
    )
    
    # Also include tasks due today (optional, based on your preference)
    # tasks_due_today = Task.objects.filter(user=user, due_date=date)
    # tasks_today = tasks_today | tasks_due_today
    
    total = tasks_today.count()
    completed = tasks_today.filter(completed=True).count()
    
    # Update the progress record
    progress.total_tasks = total
    progress.completed_tasks = completed
    progress.calculate_progress()  # This saves the record
    
    return progress

def get_weekly_progress(user, days=7):
    """Get progress data for the last N days for charting"""
    from datetime import timedelta
    
    today = timezone.now().date()
    start_date = today - timedelta(days=days-1)
    
    progress_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        progress = get_or_create_daily_progress(user, date)
        update_daily_progress(user, date)
        progress_data.append({
            'date': date.strftime('%b %d'),  # Format: "Mar 15"
            'progress': float(progress.progress_percentage),
            'completed': progress.completed_tasks,
            'total': progress.total_tasks,
        })
    
    return progress_data