# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.task_list_view, name='dashboard'),
    path('tasks/', views.task_list_view, name='task_list'),
    path('tasks/create/', views.task_create_view, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_edit_view, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete_view, name='task_delete'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle_complete_view, name='task_toggle'),
]