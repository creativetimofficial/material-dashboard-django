# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    
    path('contabilidad', views.contabilidad_view, name='contabilidad'),  # Vista de contabilidad
    path('add_ingreso', views.add_ingreso, name='add_ingreso'),
    path('add_gasto', views.add_gasto, name='add_gasto'),

]
