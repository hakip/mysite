"""mysite URL Configuration

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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls'), name="login"),
    path('register', views.RegisterView.as_view(), name='register'),
    path('admin/', admin.site.urls),
    path('polls', include('polls.urls')),
    path('blog', include('blog.urls')),
    path('mtdt', views.HomeView.as_view(), name='mtdt'),
    path('cdr', views.HomeView.as_view(), name='cdr'),
    path('pi', views.HomeView.as_view(), name='pi'),
    path('clo', views.HomeView.as_view(), name='clo'),
    path('subject', views.HomeView.as_view(), name='subject'),
    path('gradebook', views.HomeView.as_view(), name='gradebook'),
]