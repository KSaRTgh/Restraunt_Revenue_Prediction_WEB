from django.conf.urls.static import static
from django.urls import path
from .views import *
#from revpredict import settings

urlpatterns = [
    path('predict/', make_prediction, name='make-predictions'),
    path('add-to-db/',add_to_db, name='add-to-db'),
    path('add-raw-to-db/',add_raw_to_db, name='add-raw-to-db'),
    path('read-from-csv', read_from_csv, name='read-from-csv'),
]
