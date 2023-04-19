"""codio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

import codio_auth.views
from django_registration.backends.activation.views import RegistrationView
from codio_auth.forms import CodioRegistrationForm


# from django.conf import settings
# print(f"Time zone: {settings.TIME_ZONE}")
# print(f"DEBUG: {settings.DEBUG}")
# print(f"SECRET_KEY: {settings.SECRET_KEY}")
# print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
# print(f"DATABASES: {settings.DATABASES}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path("accounts/profile/", codio_auth.views.profile, name="profile"),
    path('', include('blog.urls')), 
    path(
        "accounts/register/",
        RegistrationView.as_view(form_class=CodioRegistrationForm),
        name="django_registration_register",
    ),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path("accounts/", include("allauth.urls")), # should be after 'django.contrib.auth.urls' so that login/ and other common rules are taken from there
    # path("api/v1/", include("blog.api_urls")),
    path("api/v1/", include("blog.api.urls")),
]
