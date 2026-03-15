# tasks/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 focus:outline-none focus:shadow-outline focus:border-indigo-500',
                'placeholder': 'Enter task title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 focus:outline-none focus:shadow-outline focus:border-indigo-500',
                'placeholder': 'Add details (optional)...',
                'rows': 3
            }),
            'priority': forms.Select(attrs={
                'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 focus:outline-none focus:shadow-outline focus:border-indigo-500'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'shadow border rounded w-full py-2 px-3 text-gray-700 focus:outline-none focus:shadow-outline focus:border-indigo-500'
            }),
        }