from django import forms
from .models import Ingreso, Gasto  # Importa los modelos
from .models import Campana

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['monto_ingreso']
        widgets = {
            'monto_ingreso': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['monto_gasto']
        widgets = {
            'monto_gasto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CampanaForm(forms.ModelForm):
    class Meta:
        model = Campana
        fields = ['id_campana', 'nombre_campana', 'tipo', 'estado', 'precio']
        widgets = {
            'id_campana': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_campana': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }