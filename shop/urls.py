"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import app
from app import views
from django.http import request
from django.shortcuts import redirect, HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda x: HttpResponseRedirect('index.html')),
    path('index.html', app.views.index, name='index'),
    path('login.html', app.views.logging_in, name='login_form'),
    path('logout/', app.views.logout_action, name='logout_action'),
    path('signup/', app.views.signup, name='signup_action'),
    path('product_list.html', app.views.ProductList.as_view(), name='product_list'),
    path('product_view.html', app.views.ProductView.as_view(), name='product_view'),
    path('cart.html', app.views.cart_view, name='cart'),
    path('empty_section.html', app.views.empty_section)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

