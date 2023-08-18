# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

app_name = 'home'

urlpatterns = [

    #Pagina de inicio
    path('', views.StaticPageView.as_view(), name='static_page'),
    path('inicio', views.index.as_view(), name='inicio'),
    # Inventario
    path('registrar-inventario', views.RegistrarInventarioView.as_view(), name='registrar_inventario'),
    path('listar-inventario', views.ListarInventarioView.as_view(), name='listar_inventario'),
    path('detalle-inventario/<int:pk>', views.DetalleInventarioView.as_view(), name='detalle_inventario'),

    #DASHBOARD
    path('inventario-chart', views.inventario_chart, name='inventario_chart'),

    #CALENDARIO
    path('calendario', views.Calendarioview.as_view(), name='calendario'),
    path('actualizar-evento', views.UpdateCalendarioView.as_view(), name='actualizar_evento'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
