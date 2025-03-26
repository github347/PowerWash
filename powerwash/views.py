from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, PasswordForm, SignInForm

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
            # Only display this message if the form is invalid after POST
            messages.error(request, 'Registration failed. Please try again.') 
    else: 
        form = CustomUserCreationForm()  # Initial form load for GET request

    return render(request, 'registration/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def index(request):
    form = PasswordForm()
    return render(request, 'index.html', {'form': form})

def password_view(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            return render(request, "success.html", {"message": "Password is valid!"})
        else:
            return render(request, "index.html", {"form": form})
    return render(request, "index.html", {"form": PasswordForm()})

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'sign_in.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = SignInForm()
    return render(request, 'sign_in.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def service_view(request):
    return HttpResponse("Hello, world. You're at the service page.")
