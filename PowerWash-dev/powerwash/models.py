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
        ('premium', 'Premium Detail')
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.service_type} - {self.date}"