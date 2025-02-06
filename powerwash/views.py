from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
        else:
            messages.error(request, 'Login failed. Please try again.')
    return render(request, 'registration/login.html', {})

# def register_user(request): 
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#              form.save()
#              username = form.cleaned_data.get('username') 
#              password = form.cleaned_data.get('password1') 
#              user = authenticate(request, username=username, password=password) 
#              login(request, user) 
#              messages.success(request, 'Registration successful') 
#              return redirect('home') 
#         else: 
#             messages.error(request, 'Registration failed. Please try again.') 
#     else: 
#         form = UserCreationForm() 
#     return render(request, 'registration/register.html', {'form': form})

from .forms import CustomUserCreationForm

def register_user(request): 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password1') 
            user = authenticate(request, username=username, password=password) 
            login(request, user) 
            messages.success(request, 'Registration successful') 
            return redirect('home') 
        else: 
            messages.error(request, 'Registration failed. Please try again.') 
    else: 
        form = CustomUserCreationForm() 
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    return render(request, 'home.html')
