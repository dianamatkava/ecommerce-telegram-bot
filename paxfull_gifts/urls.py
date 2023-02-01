"""paxfull_gifts URL Configuration

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
import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from dotenv import load_dotenv

from data.views import ipn_listener, update_offers

load_dotenv()

urlpatterns = [
    path('admin/', admin.site.urls),
    path(os.getenv('IPN_LISTENER'), ipn_listener),
    path('', lambda x: HttpResponse(200)),
    path('update/', update_offers)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
