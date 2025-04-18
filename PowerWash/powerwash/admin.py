from django.contrib import admin
from .models import Booking, ServicePage, Service, Profile


#Register Your Models Here, Sir/Ma'am.

admin.site.register(ServicePage)
admin.site.register(Service)
admin.site.register(Profile)
admin.site.register(Booking)