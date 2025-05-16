import requests
from django.shortcuts import render, redirect
from .models import Profile
from .forms import ClientRegisterForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from .models import Client
from django.core.exceptions import ValidationError
import re
from .validators import validate_phone_number

def register_client(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()  # Внутри save() создаются User и Profile
            Client.objects.create(profile=profile)
            login(request, profile.user)
            return redirect('mainpage')
    else:
        form = ClientRegisterForm()
    return render(request, 'registration/register_client.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                if user.is_superuser:
                    role = 'admin'
                elif hasattr(user.profile, 'master'):
                    role = 'master'
                elif hasattr(user.profile, 'client'):
                    role = 'client'
                else:
                    form.add_error(None, 'Профиль не найден.')
                    return render(request, 'registration/login_user.html', {'form': form})
                
                login(request, user)
                return redirect('mainpage')
            except Profile.DoesNotExist:
                form.add_error(None, 'Профиль не найден.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login_user.html', {'form': form})