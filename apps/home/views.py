# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse

# Modelos DDSI
from .models import Ingreso  
from .models import Gasto 
from .forms import IngresoForm, GastoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

    
@login_required(login_url="/login/")
def contabilidad_view(request):
    context = {'segment': 'contabilidad.html'}

    ingresos = Ingreso.objects.all()
    gastos = Gasto.objects.all()
    context['ingresos'] = ingresos
    context['gastos'] = gastos
    
     # Manejo de formularios para añadir ingresos y gastos
    if request.method == 'POST':
        if 'add_ingreso' in request.POST:  # Si se pulsa el botón de Ingreso
            ingreso_form = IngresoForm(request.POST)
            if ingreso_form.is_valid():
                ingreso_form.save()
                return redirect('contabilidad')  # Redirige a la misma página
        elif 'add_gasto' in request.POST:  # Si se pulsa el botón de Gasto
            gasto_form = GastoForm(request.POST)
            if gasto_form.is_valid():
                gasto_form.save()
                return redirect('contabilidad')
    else:
        ingreso_form = IngresoForm()
        gasto_form = GastoForm()
        
    context['ingreso_form'] = ingreso_form
    context['gasto_form'] = gasto_form

    
    html_template = loader.get_template('home/contabilidad.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def eliminar_ingreso(request, ingreso_id):
    # Asegurarse de que la solicitud sea POST
    if request.method == 'POST':
        ingreso = get_object_or_404(Ingreso, id_ingreso=ingreso_id)
        ingreso.delete()  # Elimina el ingreso de la base de datos

    return redirect('contabilidad')  # Redirige a la vista de contabilidad

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
                        

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
    

