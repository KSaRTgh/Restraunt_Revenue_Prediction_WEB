from django.conf.urls.static import static
from django.urls import path
from .views import *
#from revpredict import settings

urlpatterns = [
    path('dataprocessing/', dataprocessing, name='dataprocessing'),
    path('add-to-db/',add_to_db, name='add-to-db')
]
