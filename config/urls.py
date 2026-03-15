# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),        # Home page
    path('', include('accounts.urls')),    # Login, Register, Logout
    path('', include('tasks.urls')),       # Tasks & Dashboard
    path('', include('analytics.urls')),    # Analiticcs
]