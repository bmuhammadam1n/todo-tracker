# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Task
from .forms import TaskForm
from analytics.utils import update_daily_progress

@login_required
def task_list_view(request):
    # Update today's progress before showing the page
    today = timezone.now().date()
    daily_progress = update_daily_progress(request.user, today)
    
    # Get all tasks for this user
    tasks = Task.objects.filter(user=request.user)
    
    # Filters
    status_filter = request.GET.get('status')
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)
    
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    # Calculate stats for sidebar
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = total - completed
    progress = (completed / total * 100) if total > 0 else 0
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'stats': {
            'total': total,
            'completed': completed,
            'pending': pending,
            'progress': progress,
        },
        'daily_progress': daily_progress,
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_edit_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit', 'task': task})

@login_required
def task_delete_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_complete_view(request, task_id):
    """HTMX endpoint: Toggle task completion and update progress"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.htmx:
        # Toggle the task
        task.completed = not task.completed
        task.save()
        
        # Get updated progress for today
        today = timezone.now().date()
        daily_progress = update_daily_progress(request.user, today)
        
        # Get all tasks for rendering the list
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
        
        # Render the updated task list
        task_list_html = render_to_string('tasks/partials/task_list_items.html', {
            'tasks': tasks,
            'request': request
        })
        
        # Render the updated progress section
        progress_html = render_to_string('tasks/partials/progress_section.html', {
            'daily_progress': daily_progress,
            'request': request
        })
        
        # Render the updated stats section
        stats_html = render_to_string('tasks/partials/stats_section.html', {
            'daily_progress': daily_progress,
            'request': request
        })
        
        # Return all updates
        return HttpResponse(f"""
            <div id="task-list-container" hx-swap-oob="true">{task_list_html}</div>
            <div id="progress-section" hx-swap-oob="true">{progress_html}</div>
            <div id="stats-section" hx-swap-oob="true">{stats_html}</div>
        """)
    
    # Fallback for non-HTMX requests
    task.completed = not task.completed
    task.save()
    return redirect('task_list')