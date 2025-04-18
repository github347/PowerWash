from urllib import request

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ServicePage, Service, Booking  # Import your models
from django.contrib.auth import authenticate, login  # Import authentication functions
from .forms import CustomUserCreationForm, PasswordForm, SignInForm  # Import your forms
from django.http import JsonResponse
from .models import Profile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .models import UserSettings
from django.utils import timezone
from django.db import IntegrityError

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
            account_type = user.profile.account_type if hasattr(user, 'profile') else 'customer'
            if account_type == 'provider':
                return redirect('provider_dashboard')
            else:
                return redirect('customer_dashboard') # Redirect to dashboard after login
        else:
            messages.error(request, 'Login failed. Please try again.')
    return render(request, 'registration/login.html', {})


def register_user(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        account_type = request.POST.get('account_type', 'customer')  # Default to 'customer'
        if form.is_valid():
            user = form.save()  # Save the user
            # No need to manually create the profile, signals will handle it
            profile = Profile.objects.get(user=user)  # Access the profile after creation
            profile.account_type = account_type  # Update the account_type
            profile.save()  # Save the profile with the updated account_type

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, f'Registration successful as {account_type}')
            if account_type == 'provider':
                return redirect('provider_dashboard')
            else:
                return redirect('customer_dashboard')
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
    user = request.user
    bookings = Booking.objects.filter(user=user)

    # Active = pending or confirmed
    active_bookings_count = bookings.filter(status__in=['pending', 'confirmed']).count()

    # Completed services
    completed_services_count = bookings.filter(status='completed').count()

    # Total spent on completed bookings (you can customize this logic)
    total_spent = 0
    for booking in bookings.filter(status='completed'):
        if hasattr(booking, 'price'):
            total_spent += booking.price
        else:
            if booking.service_type == 'mini':
                total_spent += 29.99
            elif booking.service_type == 'full':
                total_spent += 59.99
            else:
                total_spent += 99.99

    # Loyalty points: 1 point per $10 spent (example)
    loyalty_points = int(total_spent // 10)

    # Upcoming = future + pending or confirmed
    upcoming_bookings = bookings.filter(
        status__in=['pending', 'confirmed'],
        date__gte=timezone.now().date()
    ).order_by('date', 'time')[:5]

    context = {
        'user': user,
        'active_bookings_count': active_bookings_count,
        'completed_services_count': completed_services_count,
        'total_spent': round(total_spent, 2),
        'loyalty_points': loyalty_points,
        'upcoming_bookings': upcoming_bookings,
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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check for required fields and set defaults if not provided
        if not first_name:
            first_name = user.first_name  # Keep the existing first name if no new value provided
        if not last_name:
            last_name = user.last_name  # Keep the existing last name if no new value provided

        user.first_name = first_name
        user.last_name = last_name
        user.email = request.POST.get('email', user.email)  # Default to current email if not provided
        user.save()

        # Profile update
        profile = user.profile
        profile.phone = request.POST.get('phone', profile.phone)  # Default to current profile data if not provided
        profile.address = request.POST.get('address', profile.address)
        profile.city = request.POST.get('city', profile.city)
        profile.postal_code = request.POST.get('postal_code', profile.postal_code)
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
    """Renders and handles user settings, including account deletion and settings updates."""
    # Fetch the user's settings or create them if they don't exist
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('home')
        else:
            # Handle other settings updates if needed
            email_notifications = 'email_notifications' in request.POST
            sms_notifications = 'sms_notifications' in request.POST
            marketing_comm = 'marketing_comm' in request.POST
            enable_2fa = 'enable_2fa' in request.POST
            language = request.POST.get('language', 'en')  # Default to 'en' if not selected
            time_zone = request.POST.get('time_zone', 'UTC')  # Default to 'UTC' if not selected

            # Update user settings
            user_settings.email_notifications = email_notifications
            user_settings.sms_notifications = sms_notifications
            user_settings.marketing_comm = marketing_comm
            user_settings.enable_2fa = enable_2fa
            user_settings.language = language
            user_settings.time_zone = time_zone

            # Save the updated settings
            user_settings.save()

            # Display a success message
            messages.success(request, 'Settings updated successfully!')

            # Redirect to the settings page to show updated settings
            return redirect('settings')

    # For GET request, pass the current settings to the template
    return render(request, 'dashboard/settings.html', {'user_settings': user_settings})

@login_required
def update_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile_image = request.FILES['profile_image']

        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # Create a new profile if it doesn't exist
            profile = Profile.objects.create(user=request.user)

        # Delete the old image if it exists
        if profile.profile_image:
            old_image_path = profile.profile_image.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        # Save the new image
        profile.profile_image = profile_image
        profile.save()

        # Return new image URL for the frontend
        return JsonResponse({
            'status': 'success',
            'image_url': profile.profile_image.url  # This will be the new image URL
        })
    else:
        return JsonResponse({'status': 'error'}, status=400)

@login_required
def provider_dashboard(request):

    # user = request.user
    # service_page = ServicePage.objects.filter(user=user)
    # services = service_page.service_set.all()

    return render(request, 'dashboard/provider_dashboard.html')

def create_service(request):

    return render(request, 'dashboard/create_service.html')