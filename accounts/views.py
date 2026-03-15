# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages  

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # This name must match tasks/urls.py
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"🔍 DEBUG: Attempting login for username='{username}'")  # Debug print
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"✅ DEBUG: Authentication successful for {username}")  # Debug print
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            print(f"❌ DEBUG: Authentication FAILED for username='{username}'")  # Debug print
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'registration/login.html')