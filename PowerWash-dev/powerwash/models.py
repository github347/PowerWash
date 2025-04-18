from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_comm = models.BooleanField(default=False)
    enable_2fa = models.BooleanField(default=False)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('es', 'Español'), ('fr', 'Français')], default='en')
    time_zone = models.CharField(max_length=50, choices=[('UTC', 'UTC (GMT+0)'), ('EST', 'Eastern Time (GMT-5)'), ('PST', 'Pacific Time (GMT-8)')], default='UTC')

    def __str__(self):
        return f"Settings for {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print("create_user_profile called")
    if created:
        print("user created, creating profile")
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("save_user_profile called")
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        print("Profile does not exist, creating profile")
        Profile.objects.create(user=instance)

class ServicePage(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()

    def __str__(self):
        return self.title

class Service(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    SERVICE_CHOICES = [
        ('mini', 'Mini Valet'),
        ('full', 'Full Valet'),
        ('premium', 'Wax and Polish')
    ]
    
    VEHICLE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('van', 'Van')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    LOCATION_CHOICES = [
        ('miami', 'Miami - 1250 Ocean Drive, Miami Beach, FL 33139'),
        ('orlando', 'Orlando - 8955 International Drive, Orlando, FL 32819'),
        ('tampa', 'Tampa - 615 Channelside Drive, Tampa, FL 33602'),
        ('jacksonville', 'Jacksonville - 2 Independent Drive, Jacksonville, FL 32202'),
        ('tallahassee', 'Tallahassee - 200 S Adams St, Tallahassee, FL 32301'),
        ('gainesville', 'Gainesville - 3600 SW Archer Rd, Gainesville, FL 32608'),
        ('pensacola', 'Pensacola - 400 Pensacola Beach Blvd, Gulf Breeze, FL 32561'),
        ('fortlauderdale', 'Fort Lauderdale - 1100 Seabreeze Blvd, Fort Lauderdale, FL 33316'),
        ('daytona', 'Daytona Beach - 1200 Main St, Daytona Beach, FL 32118'),
        ('keywest', 'Key West - 400 Front Street, Key West, FL 33040'),
        ('naples', 'Naples - 955 5th Avenue South, Naples, FL 34102')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.service_type} - {self.date}"