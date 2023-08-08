from django import forms
from apps.home.models import Inventario, EventoCaledario


#crea formulario para registarr inventario
class RegistrarInventarioForm(forms.ModelForm):
    class Meta:
            model = Inventario
            fields = ('nombre', 'descripcion', 'cantidad', 'precio', 'categoria', 'estado')
            widgets = {
                'nombre': forms.TextInput(attrs={'class': 'form-control'}),
                'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
                'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
                'precio': forms.TextInput(attrs={'class': 'form-control'}),
                'categoria': forms.TextInput(attrs={'class': 'form-control'}),
                'estado': forms.Select(attrs={'class': 'form-control'}),  # Usamos forms.Select para el campo "estado"
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].widget.attrs.update({'class': 'form-control'})

class EventoCalendarioForm(forms.ModelForm):

    class Meta:
        model = EventoCaledario
        fields = ('titulo', 'descripcion', 'fecha_inicio')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super(EventoCalendarioForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})

