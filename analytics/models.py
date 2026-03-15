# analytics/models.py
from django.db import models
from django.conf import settings

class DailyProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_progress'
    )
    date = models.DateField(unique=True)  # One record per user per day
    total_tasks = models.PositiveIntegerField(default=0)
    completed_tasks = models.PositiveIntegerField(default=0)
    progress_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']  # Ensure one record per user per day
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.progress_percentage}%"
    
    def calculate_progress(self):
        """Calculate and update progress percentage"""
        if self.total_tasks > 0:
            self.progress_percentage = (self.completed_tasks / self.total_tasks) * 100
        else:
            self.progress_percentage = 0
        self.save()
        return self.progress_percentage