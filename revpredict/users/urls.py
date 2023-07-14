from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    #path('registration/', registration, name='registration'),
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path('register/', sign_up, name='register'),
]

