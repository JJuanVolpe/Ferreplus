from django import forms
from .models import Product, Rating
from datetime import time,datetime

class crear_intercambio_con_espera_de_ofertas(forms.Form):
    nombre = forms.CharField(label="nombre",max_length=200)
    estado = forms.CharField(label="estado",max_length=200)
    categoria = forms.CharField(label="categoria",max_length=200)
    foto = forms.ImageField()
    descripcion = forms.CharField(label="descripcion",max_length=200)
    modelo = forms.CharField(label="modelo",max_length=200)
    marca = forms.CharField(label="marca",max_length=200)
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        ESTADO_CHOICES = [
            ('nuevo', 'Nuevo'),
            ('usado', 'Usado'),
        ]
        fields = ['nombre', 'estado', 'categoria','marca','modelo', 'foto', 'descripcion','hora','fecha']
        widgets = {
            'estado': forms.Select(attrs={'class': 'selectEstado'},choices=ESTADO_CHOICES),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'timepicker'}),
        }
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['hora'].required = True
        self.fields['fecha'].required = True
        self.fields['descripcion'].required = False
        self.fields['marca'].required = False
        self.fields['modelo'].required = False

class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del Proyect", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))


class RecoveryForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', required=True, max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Introduzca el correo asociado a una cuenta existente', 'autocomplete':'on'}))


class PopupForm(forms.Form):
    message = forms.CharField(label='Mensaje del Popup', max_length=100)


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }