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
from django.urls import path, include
from . import views
from powerwash.views import sign_in_view, login_view  # Import the login view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('', views.home, name='home'),
    path('sign-in/', sign_in_view, name='sign_in'),  # Sign-in page
    path('login/', login_view, name='login'),  # Login route
    path('', views.index, name='index'),  # Home page route
    path('validate-password/', views.password_view, name='password_view'),  # Password validation route
]
