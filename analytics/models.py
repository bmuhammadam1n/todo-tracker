# analytics/models.py
from django.db import models
from django.conf import settings

# analytics/models.py
class DailyProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_progress'
    )
    # ⚠️ REMOVE unique=True from here:
    date = models.DateField()  # ← Changed: removed unique=True
    
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
        # ✅ This is the correct constraint: unique per USER per DATE
        unique_together = ['user', 'date']  # ← Keep this!
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.progress_percentage}%"
    
    def calculate_progress(self):
        if self.total_tasks > 0:
            self.progress_percentage = (self.completed_tasks / self.total_tasks) * 100
        else:
            self.progress_percentage = 0
        self.save()
        return self.progress_percentage