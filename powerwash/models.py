from django.db import models
from django.contrib.auth.models import User

class ServicePage(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()

    def __str__(self):
        return self.title

class Service(models.Model):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE) #Deletes all services within a service page when the page is deleted
    name = models.CharField(max_length=120)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name