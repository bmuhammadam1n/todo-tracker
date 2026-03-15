# analytics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('analytics/', views.analytics_dashboard_view, name='analytics'),
    path('history/', views.history_view, name='history'),
    path('api/heatmap/', views.heatmap_data_view, name='heatmap_data'),  # Add this
]