from django.urls import path
from search.views import *


urlpatterns = ([
    path('', search, name='search'),
    path('<str:title_quest>/', search, name='search'),
])
