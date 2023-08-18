# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView, DetailView, UpdateView

#Propios
from apps.home.forms import *
from django.shortcuts import render

from apps.home.models import EventoCaledario


class index(LoginRequiredMixin, View):

    total_inventario = Inventario.objects.all().count()
    inventario = Inventario.objects.all()

    context = {'segment': 'index',
               'total_inventario': total_inventario,
               'inventario': inventario,}
    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html', self.context)


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

        html_template = loader.get_template('layouts/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('layouts/page-500.html')
        return HttpResponse(html_template.render(context, request))


class RegistrarInventarioView(FormView):

    template_name = 'home/registrar_inventario_form.html'
    form_class = RegistrarInventarioForm
    success_url = '/registrar-inventario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activo'] = True
        return context

    def form_valid(self, form):
        #validar que el estado se activo sino no se guarda
        if form.cleaned_data['estado'] == 2:
            messages.error(self.request, 'No se puede guardar un inventario inactivo')
            return super().form_invalid(form)
        form.save()
        messages.success(self.request, 'El inventario se ha registrado exitosamente.')
        return super().form_valid(form)


class ListTableView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = Inventario.objects.all()
        context['actions'] = self.actions
        context['column_names'] = self.column_names
        context['fields'] = self.fields
        context['activo_listar'] = True
        return context

class ListarInventarioView(ListTableView):

    template_name = 'home/listar_inventario.html'
    column_names = ['Nombre', 'Descripción', 'Cantidad', 'Precio', 'Estado']
    fields = ['nombre', 'descripcion', 'cantidad', 'precio', 'estado']
    model = Inventario

    actions = [
        {
            'url': 'home:detalle_inventario',
            'url_args': 'pk',
            'title': 'Ver',
            'icon': 'eye',
            'color': 'primary',
        },
    ]


class DetalleInventarioView(DetailView):

    template_name = 'home/detalle_inventario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventario'] = Inventario.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        return Inventario.objects.all()

def inventario_chart(request):
    # Obtener los datos del inventario desde la base de datos
    inventarios = Inventario.objects.all()

    # Crear diccionario para almacenar la cantidad de inventario por categoría
    inventario_por_categoria = {}

    for inventario in inventarios:
        categoria = inventario.categoria
        cantidad = inventario.cantidad

        if categoria in inventario_por_categoria:
            inventario_por_categoria[categoria] += cantidad
        else:
            inventario_por_categoria[categoria] = cantidad

    # Convertir el diccionario en listas para utilizarlo en el gráfico
    categorias = list(inventario_por_categoria.keys())
    cantidades = list(inventario_por_categoria.values())

    return JsonResponse({'categorias': categorias, 'cantidades': cantidades})


class Calendarioview(TemplateView, FormView):

    template_name = 'home/calendar.html'
    form_class = EventoCalendarioForm
    success_url = '/calendario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos'] = EventoCaledario.objects.all()
        context['activo_calendario'] = True
        return context

    def form_valid(self, form):
        evento = form.save(commit=False)
        evento.save()
        messages.success(self.request, 'El evento se ha registrado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors
        for error in errors:
            messages.error(self.request, 'Se ha producido un error en el formulario.')
        return super().form_invalid(form)

class UpdateCalendarioView(View):

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            try:
                id = request.POST.get('id')
                fecha_inicio = request.POST.get('start')
                evento = EventoCaledario.objects.get(pk=id)
                evento.fecha_inicio = fecha_inicio
                evento.save()
                return JsonResponse({'status': 'success'})
            except:
                return JsonResponse({'status': 'error'})

class StaticPageView(TemplateView):

    template_name = 'static_page/static_page.html'


