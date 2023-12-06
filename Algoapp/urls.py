from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),

    path('subscribe/', subscribe, name='subscribe'),

    path('register/', register, name='register'),

    path('login/', user_login, name='login'),  # Add the login URL

    path('logout/', user_logout, name='logout'),  # Add the logout URL

    path('checkout_success/', checkout_success, name='checkout_success'),

    path('active_subscription/', active_subscription, name='active_subscription'),

    path('newsLetter/', newsLetter, name='newsLetter'),

    path('contactus/', contactUs, name='contactUs'),

    path('aboutus/', aboutus, name='aboutus'),

    path('terms/', terms, name='terms'),

    path('privacy/', privacy, name='privacy'),

    path('questions/', questions, name='questions'),

    path('allposts/', allblogs, name='allposts'),

    path('singlepost/<int:id>/', singleblogs, name='singlepost'),

    path('allplans/', allplans, name='allplans'),

    path('freetrile/<int:id>/', clime_free_trile, name='clime_free_trile'),

    path('otpvarification/', otpvarification, name='otpvarification'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)