# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render

# Modelos DDSI
from .models import Ingreso  
from .models import Gasto 
from .forms import IngresoForm, GastoForm



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
    
    
    
    

def contabilidad_view(request):
    ingresos = Ingreso.objects.all()  # Extrae todos los ingresos
    gastos = Gasto.objects.all()      # Extrae todos los gastos

    return render(request, 'contabilidad.html', {
        'ingresos': ingresos,
        'gastos': gastos,
    })

def add_ingreso(request):
    if request.method == "POST":
        form = IngresoForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/contabilidad.html")

    else:
        form = IngresoForm()

    return render(request, "ejemplo.html", {"ingreso_form": form})
    

def add_gasto(request):
    if request.method == "POST":
        form = GastoForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/contabilidad.html")

    else:
        form = GastoForm()

    return render(request, "contabilidad.html", {"gasto_form": form})