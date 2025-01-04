# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.db.models import Sum
from django.db.models import Q

# Modelos DDSI
from .models import Ingreso  
from .models import Gasto 
from .forms import IngresoForm, GastoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Campana
from .forms import CampanaForm


def contabilidad_view(request):
      # Calcular la suma de los ingresos
    total_ingresos = Ingreso.objects.all().aggregate(total=Sum('monto_ingreso'))['total'] or 0

    # Calcular la suma de los gastos
    total_gastos = Gasto.objects.all().aggregate(total=Sum('monto_gasto'))['total'] or 0

    # Calcular el balance neto
    balance_neto = total_ingresos - total_gastos

    # Pasar todo al contexto
    return render(request, 'home/contabilidad.html', {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance_neto': balance_neto,
    })
    
@login_required(login_url="/login/")
def ingresos_view(request):
    # BUSCAR INGRESOS
    search_query = request.GET.get('search', '')
    if search_query:
        ingresos = Ingreso.objects.filter(id_ingreso__icontains=search_query)
    else:
        ingresos = Ingreso.objects.all()

    context = {
        'ingresos': ingresos,
    }

    # Manejo de formularios para anadir ingresos y gastos
    if request.method == 'POST':
        if 'add_ingreso' in request.POST:  # Si se pulsa el botón de Ingreso
            ingreso_form = IngresoForm(request.POST)
            if ingreso_form.is_valid():
                ingreso_form.save()
                return redirect('ingresos')  # Redirige a la misma página
        elif 'edit_ingreso' in request.POST:  # Si se pulsa el botón de Editar
            # Obtener el id del ingreso desde el formulario POST
            ingreso_id = request.POST.get('ingreso_id')  # El ID viene con el formulario
            ingreso = get_object_or_404(Ingreso, id_ingreso=ingreso_id)
            ingreso_form = IngresoForm(request.POST, instance=ingreso)
            if ingreso_form.is_valid():
                ingreso_form.save()
                return redirect('ingresos')  # Redirige a la misma página
    else:
        ingreso_form = IngresoForm()

    # Si estamos editando un ingreso, obtenemos ese ingreso
    ingreso_id = request.GET.get('edit', None)
    if ingreso_id:
        ingreso = get_object_or_404(Ingreso, id_ingreso=ingreso_id)
        ingreso_form = IngresoForm(instance=ingreso)

    context['ingreso_form'] = ingreso_form

    html_template = loader.get_template('home/ingresos.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def gastos_view(request):
    # BUSCAR GASTOS
    search_query = request.GET.get('search', '')
    if search_query:
        gastos = Gasto.objects.filter(id_gasto__icontains=search_query)
    else:
        gastos = Gasto.objects.all()

    context = {
        'gastos': gastos,
    }

    # Manejo de formularios para anadir gastos y gastos
    if request.method == 'POST':
        if 'add_gasto' in request.POST:  # Si se pulsa el botón de Gasto
            gasto_form = GastoForm(request.POST)
            if gasto_form.is_valid():
                gasto_form.save()
                return redirect('gastos')  # Redirige a la misma página
        elif 'edit_gasto' in request.POST:  # Si se pulsa el botón de Editar
            # Obtener el id del gasto desde el formulario POST
            gasto_id = request.POST.get('gasto_id')  # El ID viene con el formulario
            gasto = get_object_or_404(Gasto, id_gasto=gasto_id)
            gasto_form = GastoForm(request.POST, instance=gasto)
            if gasto_form.is_valid():
                gasto_form.save()
                return redirect('gastos')  # Redirige a la misma página
    else:
        gasto_form = GastoForm()

    # Si estamos editando un gasto, obtenemos ese gasto
    gasto_id = request.GET.get('edit', None)
    if gasto_id:
        gasto = get_object_or_404(Gasto, id_gasto=gasto_id)
        gasto_form = GastoForm(instance=gasto)

    context['gasto_form'] = gasto_form

    html_template = loader.get_template('home/gastos.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def eliminar_ingreso(request, ingreso_id):
    # Asegurarse de que la solicitud sea POST
    if request.method == 'POST':
        ingreso = get_object_or_404(Ingreso, id_ingreso=ingreso_id)
        ingreso.delete()  # Elimina el ingreso de la base de datos

    return redirect('contabilidad')  # Redirige a la vista de contabilidad

@login_required(login_url="/login/")
def eliminar_gasto(request, gasto_id):
    # Asegurarse de que la solicitud sea POST
    if request.method == 'POST':
        gasto = get_object_or_404(Gasto, id_gasto=gasto_id)
        gasto.delete()  # Elimina el ingreso de la base de datos

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
    
    
@login_required(login_url="/login/")
def listar_campanas(request):
    search_query = request.GET.get('search', '')
    if search_query:
        campanas = Campana.objects.filter(
            Q(nombre_campana__icontains=search_query) |
            Q(tipo__icontains=search_query) |
            Q(estado__icontains=search_query)
        )
    else:
        campanas = Campana.objects.all()

    context = {
        'campanas': campanas,
    }

    return render(request, 'home/listar_campanas.html', context)

@login_required(login_url="/login/")
def dar_de_alta_campana(request):
    if request.method == 'POST':
        campana_form = CampanaForm(request.POST)
        if campana_form.is_valid():
            campana_form.save()
            return redirect('listar_campanas')  # Redirect alla lista delle campagne
    else:
        campana_form = CampanaForm()

    context = {
        'campana_form': campana_form
    }

    return render(request, 'home/dar_de_alta_campana.html', context)

@login_required(login_url="/login/")
def modificar_campana(request, campana_id):
    campana = get_object_or_404(Campana, id_campana=campana_id)

    if request.method == 'POST':
        campana_form = CampanaForm(request.POST, instance=campana)
        if campana_form.is_valid():
            campana_form.save()
            return redirect('listar_campanas')  # Redirect alla lista delle campagne
    else:
        campana_form = CampanaForm(instance=campana)

    context = {
        'campana_form': campana_form,
        'campana': campana
    }

    return render(request, 'home/modificar_campana.html', context)

@login_required(login_url="/login/")
def eliminar_campana(request, campana_id):
    campana = get_object_or_404(Campana, id_campana=campana_id)
    campana.delete()
    return redirect('listar_campanas')  # Redirect alla lista delle campagne