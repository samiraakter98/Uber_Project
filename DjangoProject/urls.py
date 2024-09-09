"""DjangoProject URL Configuration

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
import pr.views as pr_views
import login.views as login_views
import driver.views as driver_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ACCIDENT', pr_views.list_accidents),
    path('login',login_views.login,name="welcome"),
    path('login1',login_views.login1, name="l"),
    path('signup',login_views.signup, name="s"),
    path('signup_driver',login_views.signup_driver, name="sd"),
    path('user_login',login_views.user_login, name="map1"),
    path('user_driver_map',login_views.user_driver_map, name="map2"),
    path('confirmation',login_views.confirmation, name="map3"),
    path('driver_profile', driver_views.driver_profile,name="driver_page"),
    path('accident', login_views.accident, name="accident"),
    path('trans_accident', login_views.trans_accident, name="trans_accident"),
    path('accident_report', login_views.accident_report, name="report"),
    path('user_profile_trip', login_views.user_profile_trip, name="user_p_t"),
    path('rating',login_views.rating,name="rating"),
    path('payment',login_views.payment),
    path('payment_page',login_views.payment_page,name="payment_page"),
    path('for_trip_info',login_views.for_trip_info),
    path('payment_bkash',login_views.payment_bkash,name="bkash"),
    path('payment_rocket',login_views.payment_rocket,name="rocket"),
    path('payment_nexus',login_views.payment_nexus,name="nexus"),
    path('payment_cash',login_views.payment_cash,name="cash"),

]
