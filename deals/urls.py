from django.contrib import admin
from django.urls import path, re_path



from .views import *

urlpatterns = [
path('', home, name='home'),
path('best/<int:price>/<int:days>/<int:datavalue>/<int:callvalue>/<int:smsvalue>', solutions, name='solutions'),
path('list/', list, name='list'),
path('about/', about, name='about'),
    ]
