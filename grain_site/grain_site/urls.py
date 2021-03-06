"""grain_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import wallet.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('wallet/<slug:wslug>/', views.wallet, name='wallet'),
    path('clan/<slug:cslug>/<slug:cwslug>/topup', views.clanwallet_topup, name='clanwallet_topup'),
    path('clan/<slug:cslug>/<slug:cwslug>/withdraw', views.clanwallet_withdraw, name='clanwallet_withdraw'),
    path('clan/<slug:cslug>', views.clan, name='clan'),
    path('under_construction_template', views.under_construction, name='under_construction'),
    path('', views.main, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)