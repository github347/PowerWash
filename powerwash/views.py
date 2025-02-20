from django.shortcuts import render
from .forms import PasswordForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    form = PasswordForm()
    return render(request, 'index.html', {'form': form})

def password_view(request):
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            # Success case: Render a success page or the same page with a success message
            return render(request, "success.html", {"message": "Password is valid!"})
        else:
            # Failure case: Render the form with errors on the same page
            return render(request, "index.html", {"form": form})
    
    # For GET request or if no form submitted
    return render(request, "index.html", {"form": PasswordForm()})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignInForm

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to a success page
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
            return redirect("home") # home needs to be the actual url
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")