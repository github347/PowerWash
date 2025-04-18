from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking
from datetime import datetime

@login_required
def customer_dashboard(request):
    # Get upcoming bookings for the current user
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        date__gte=datetime.now().date()
    ).order_by('date', 'time')

    # Get past bookings for the current user
    past_services = Booking.objects.filter(
        user=request.user,
        date__lt=datetime.now().date()
    ).order_by('-date', '-time')

    # Calculate loyalty points (1 point per booking)
    loyalty_points = past_services.count() * 10

    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_services': past_services,
        'loyalty_points': loyalty_points,
    }
    
    return render(request, 'dashboard/customer_dashboard.html', context)

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    
    booking_stats = {
        'all': bookings.count(),
        'completed': bookings.filter(status='completed').count(),
        'pending': bookings.filter(status='pending').count(),
        'cancelled': bookings.filter(status='cancelled').count(),
    }
    
    context = {
        'bookings': bookings,
        'booking_stats': booking_stats,
    }
    
    return render(request, 'dashboard/history.html', context)