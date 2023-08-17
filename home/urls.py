# from django.urls import path
from . import views
from django.urls import path,include
urlpatterns = [
    path('generate-referral-link/', views.generate_referral_link.as_view(), name='generate_referral_link'),
    path('referral/<str:referral_code>/', views.login_with_referral.as_view(), name='login_with_referral'),
    path('referrals/', views.checkthereferals.as_view(), name='checkthereferals'),
    # Add more URL patterns for your other views here
]
