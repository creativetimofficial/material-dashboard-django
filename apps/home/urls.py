# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    
    path('contabilidad', views.contabilidad_view, name='contabilidad'), 
    path('eliminar_ingreso/<int:ingreso_id>/', views.eliminar_ingreso, name='eliminar_ingreso'),    
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    
]
