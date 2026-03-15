# analytics/views.py
from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import DailyProgress
from .utils import get_weekly_progress
from tasks.models import Task


@login_required
def analytics_dashboard_view(request):
    """Main analytics page with charts"""
    user = request.user
    today = timezone.now().date()
    
    # Get last 30 days of progress data
    progress_data = get_weekly_progress(user, days=30)
    
    # Calculate weekly stats
    week_ago = today - timedelta(days=7)
    weekly_progress = DailyProgress.objects.filter(
        user=user,
        date__gte=week_ago,
        date__lte=today
    )
    
    weekly_avg = weekly_progress.aggregate(
        avg_progress=models.Avg('progress_percentage')
    )['avg_progress'] or 0
    
    # Calculate monthly stats
    month_ago = today - timedelta(days=30)
    monthly_progress = DailyProgress.objects.filter(
        user=user,
        date__gte=month_ago,
        date__lte=today
    )
    
    monthly_avg = monthly_progress.aggregate(
        avg_progress=models.Avg('progress_percentage')
    )['avg_progress'] or 0
    
    # Total tasks ever completed
    total_completed = Task.objects.filter(
        user=user,
        completed=True
    ).count()
    
    # Total tasks ever created
    total_created = Task.objects.filter(
        user=user
    ).count()
    
    # Best day (highest completion)
    best_day = DailyProgress.objects.filter(
        user=user,
        progress_percentage=100
    ).order_by('-date').first()
    
    # Current streak (consecutive days with tasks)
    streak = calculate_streak(user, today)
    
    context = {
        'progress_data': progress_data,
        'weekly_avg': weekly_avg,
        'monthly_avg': monthly_avg,
        'total_completed': total_completed,
        'total_created': total_created,
        'best_day': best_day,
        'streak': streak,
    }
    return render(request, 'analytics/analytics_dashboard.html', context)

@login_required
def history_view(request):
    """View past progress by date"""
    user = request.user
    
    # Get selected date (default to today)
    selected_date = request.GET.get('date', timezone.now().date())
    
    # Get progress for selected date
    try:
        daily_progress = DailyProgress.objects.get(
            user=user,
            date=selected_date
        )
    except DailyProgress.DoesNotExist:
        daily_progress = None
    
    # Get tasks for selected date
    tasks_on_date = Task.objects.filter(
        user=user,
        created_at__date=selected_date
    )
    
    # Get last 7 days for quick navigation
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    
    context = {
        'selected_date': selected_date,
        'daily_progress': daily_progress,
        'tasks_on_date': tasks_on_date,
        'last_7_days': last_7_days,
        'today': today,
    }
    return render(request, 'analytics/history.html', context)

def calculate_streak(user, today):
    """Calculate current day streak"""
    streak = 0
    current_date = today
    
    while True:
        progress = DailyProgress.objects.filter(
            user=user,
            date=current_date,
            total_tasks__gt=0
        ).first()
        
        if progress:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak

# analytics/views.py - Add this function

@login_required
def heatmap_data_view(request):
    """Return heatmap data as JSON for the last 365 days"""
    from django.http import JsonResponse
    from datetime import timedelta
    
    user = request.user
    today = timezone.now().date()
    start_date = today - timedelta(days=364)
    
    heatmap_data = []
    
    for i in range(365):
        date = start_date + timedelta(days=i)
        progress = DailyProgress.objects.filter(
            user=user,
            date=date
        ).first()
        
        if progress and progress.total_tasks > 0:
            level = 0
            if progress.progress_percentage == 100:
                level = 4
            elif progress.progress_percentage >= 75:
                level = 3
            elif progress.progress_percentage >= 50:
                level = 2
            elif progress.progress_percentage > 0:
                level = 1
            
            heatmap_data.append({
                'date': date.isoformat(),
                'count': progress.completed_tasks,
                'level': level,
                'progress': float(progress.progress_percentage),
            })
        else:
            heatmap_data.append({
                'date': date.isoformat(),
                'count': 0,
                'level': 0,
                'progress': 0,
            })
    
    return JsonResponse({'heatmap': heatmap_data})
