"""
URL configuration for powerwash project.
# powerwash/urls.py
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from powerwash.views import sign_in_view, login_view  # Import the login view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('sign-in/', sign_in_view, name='sign_in'),  # Sign-in page
    path('login/', login_view, name='login'),  # Login route
    path('', views.index, name='index'),  # Home page route
    path('validate-password/', views.password_view, name='password_view'),  # Password validation route
    path('service-view/<str:title>', views.service_view, name='service_view'), # Service page from service provider
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/p', views.provider_dashboard, name='provider_dashboard'),
    path('dashboard/booking/', views.booking_view, name='booking'),
    path('dashboard/history/', views.history_view, name='history'),
    path('dashboard/history/rebook/<int:booking_id>/', views.rebook_service, name='rebook_service'),
    path('dashboard/history/review/<int:booking_id>/', views.leave_review, name='leave_review'),
    path('dashboard/profile/', views.profile_view, name='profile'),
    path('dashboard/settings/', views.settings_view, name='settings'),
    path('update-profile-image/', views.update_profile_image, name='update_profile_image'),
    path('dashboard/create-service/', views.create_service, name='create_service')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)