from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ServicePage, Service, Booking  # Import your models
from django.contrib.auth import authenticate, login  # Import authentication functions
from .forms import CustomUserCreationForm, PasswordForm, SignInForm  # Import your forms

# View for user login
def login_user(request):
    """Handles user login."""
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

# View for user registration
def register_user(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')  # Corrected to password2
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# View for the home page
def home(request):
    """Renders the home page."""
    return render(request, 'home.html')

# View for the index page (password form example)
def index(request):
    """Renders the index page with a password form."""
    form = PasswordForm()
    return render(request, 'index.html', {'form': form})

# View for password form processing
def password_view(request):
    """Handles password form submission."""
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            return render(request, "success.html", {"message": "Password is valid!"})
        else:
            return render(request, "index.html", {"form": form})
    return render(request, "index.html", {"form": PasswordForm()})

# View for sign-in page (alternative login)
def sign_in_view(request):
    """Renders the sign-in page."""
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

# View for login (alternative)
def login_view(request):
    """Renders the login page."""
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

# View for service page
def service_view(response, title):
    """Renders a service page."""
    sp = ServicePage.objects.get(title=title)
    s = sp.service_set.get(id=1)
    return render(response, "powerwash/service.html", {})

# View for customer dashboard (requires login)
@login_required
def customer_dashboard(request):
    """Renders the customer dashboard."""
    context = {
        'user': request.user,
        'active_bookings_count': 0,  # Add logic to calculate
        'completed_services_count': 0,  # Add logic to calculate
        'total_spent': 0.00,  # Add logic to calculate
        'loyalty_points': 0,  # Add logic to calculate
        'upcoming_bookings': []  # Add logic to calculate
    }
    return render(request, 'dashboard/customer_dashboard.html', context)

# View for booking a service (requires login)
@login_required
def booking_view(request):
    """Handles booking a service."""
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

# View for booking history (requires login)
@login_required
def history_view(request):
    """Renders the booking history."""
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    booking_stats = {
        'all': bookings.count(),
        'pending': bookings.filter(status='pending').count(),
        'completed': bookings.filter(status='completed').count(),
        'cancelled': bookings.filter(status='cancelled').count()
    }
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

# View for rebooking a service (requires login)
@login_required
def rebook_service(request, booking_id):
    """Handles rebooking a service."""
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

# View for leaving a review (requires login)
@login_required
def leave_review(request, booking_id):
    """Handles leaving a review for a booking."""
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        # Add review logic here (e.g., save review to a Review model)
        messages.success(request, 'Review submitted successfully!')
        return redirect('history')
    return redirect('history')

# View for user profile (requires login)
@login_required
def profile_view(request):
    """Renders and updates the user profile."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        profile = user.profile
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.postal_code = request.POST.get('postal_code')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    context = {
        'total_bookings': Booking.objects.filter(user=request.user).count(),
        'completed_services': Booking.objects.filter(user=request.user, status='completed').count(),
        'loyalty_points': 0,  # Implement logic
        'recent_activities': []  # Implement logic
    }
    return render(request, 'dashboard/profile.html', context)

# View for user settings (requires login)
@login_required
def settings_view(request):
    """Renders and handles user settings, including account deletion."""
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('home')
        else:
            # Handle other settings updates if needed
            messages.success(request, 'Settings updated successfully!')
            return redirect('settings')
    return render(request, 'dashboard/settings.html')
    