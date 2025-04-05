from django.db import models
from django.contrib.auth.models import User

#Service Page model. Should be one per user.
#TODO: Flesh out the features and specific details.
class ServicePage(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()

    def __str__(self):
        return self.title

#Different services within a service page.
class Service(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE) #Deletes all services within a service page when the page is deleted
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