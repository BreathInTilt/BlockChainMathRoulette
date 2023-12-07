"""
URL configuration for Roulette1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Roulette import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_roulette_page, name='home'),
    path('refill', views.show_refill_page, name='refill'),
    path('top_up_small', views.top_up_small, name='top_up_small'),
    path('top_up_medium', views.top_up_medium, name='top_up_medium'),
    path('top_up_large', views.top_up_large, name='top_up_large'),
    path('update_balance', views.update_balance, name='update_balance'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('submit_withdrawal', views.submit_withdrawal, name='submit_withdrawal')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
