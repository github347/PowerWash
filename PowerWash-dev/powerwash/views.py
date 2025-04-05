from http.client import responses

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, PasswordForm, SignInForm
from .models import ServicePage, Service, Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('customer_dashboard')  # Redirect to dashboard after login
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

def service_view(response, title):
    sp = ServicePage.objects.get(title=title)
    s = sp.service_set.get(id=1)
    return render(response, "powerwash/service.html", {})

@login_required
def customer_dashboard(request):
    context = {
        'user': request.user,
        'active_bookings_count': 0,
        'completed_services_count': 0,
        'total_spent': 0.00,
        'loyalty_points': 0,
        'upcoming_bookings': []
    }
    return render(request, 'dashboard/customer_dashboard.html', context)

@login_required
def booking_view(request):
    if request.method == 'POST':
        try:
            booking = Booking(
                user=request.user,
                service_type=request.POST['service_type'],
                vehicle_type=request.POST['vehicle_type'],
                date=request.POST['date'],
                time=request.POST['time'],
                special_requests=request.POST.get('special_requests', '')
            )
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('customer_dashboard')
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    return render(request, 'dashboard/booking.html')

@login_required
def history_view(request):
    # Get all bookings for the current user
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    
    # Count bookings by status
    booking_stats = {
        'all': bookings.count(),
        'pending': bookings.filter(status='pending').count(),
        'completed': bookings.filter(status='completed').count(),
        'cancelled': bookings.filter(status='cancelled').count()
    }
    
    # Add price field if not exists
    for booking in bookings:
        if not hasattr(booking, 'price'):
            if booking.service_type == 'mini':
                booking.price = 29.99
            elif booking.service_type == 'full':
                booking.price = 59.99
            else:
                booking.price = 99.99
    
    context = {
        'bookings': bookings,
        'booking_stats': booking_stats,
    }
    return render(request, 'dashboard/history.html', context)

@login_required
def rebook_service(request, booking_id):
    try:
        original_booking = Booking.objects.get(id=booking_id, user=request.user)
        new_booking = Booking.objects.create(
            user=request.user,
            service_type=original_booking.service_type,
            vehicle_type=original_booking.vehicle_type,
            special_requests=original_booking.special_requests,
            status='pending'
        )
        messages.success(request, 'Service rebooked successfully!')
        return redirect('booking')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('history')

@login_required
def leave_review(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        # Add review logic here
        messages.success(request, 'Review submitted successfully!')
        return redirect('history')
    return redirect('history')

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # Update profile information
        profile = user.profile
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.postal_code = request.POST.get('postal_code')
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    # Get statistics
    context = {
        'total_bookings': Booking.objects.filter(user=request.user).count(),
        'completed_services': Booking.objects.filter(user=request.user, status='completed').count(),
        'loyalty_points': 0,  # Implement your loyalty points logic
        'recent_activities': []  # Implement your recent activities logic
    }
    
    return render(request, 'dashboard/profile.html', context)

@login_required
def settings_view(request):
    if request.method == 'POST':
        # Handle settings update
        user = request.user
        # Update user settings
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    return render(request, 'dashboard/settings.html')