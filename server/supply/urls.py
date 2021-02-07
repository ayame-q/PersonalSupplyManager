"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('supply/<slug:pk>', views.SupplyRetrieveUpdateAPIView.as_view()),
    path('supply/search', views.SupplySearchAPIView.as_view()),
    path('supply/search/<slug:full_number>', views.SupplySearchAPIView.as_view()),
    path('user/', views.UserListAPIView.as_view()),
    path('standard/', views.StandardListCreateAPIView.as_view()),
    path('standard/<int:pk>', views.StandardRetrieveUpdateDestroyAPIView.as_view()),
    path('connector/', views.ConnectorListCreateAPIView.as_view()),
    path('connector/<int:pk>', views.ConnectorRetrieveUpdateDestroyAPIView.as_view()),
]
