from django import forms
from .models import Product, Rating, Sucursal
from datetime import time,datetime
from datetime import date


class CrearIntercambioForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=200)
    estado = forms.ChoiceField(label="Estado", choices=[('Nuevo', 'Nuevo'), ('Usado', 'Usado')], initial='Usado')
    categoria = forms.CharField(label="Categoría", max_length=200)
    foto = forms.ImageField(label="Foto")
    descripcion = forms.CharField(label="Descripción", max_length=200, required=False, widget=forms.Textarea(attrs={'maxlength': '150'}))
    modelo = forms.CharField(label="modelo", max_length=200, required=False)
    marca = forms.CharField(label="marca", max_length=200, required=False)
    sucursal = forms.ModelChoiceField(label="Sucursal donde realizar el intercambio", queryset=Sucursal.objects.all(), empty_label="Seleccione una sucursal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases CSS a los campos de formulario
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        ESTADO_CHOICES = [
            ('nuevo', 'Nuevo'),
            ('usado', 'Usado'),
        ]
        fields = ['nombre', 'estado', 'categoria','marca','modelo', 'foto', 'descripcion','hora','fecha']
        widgets = {
            'estado': forms.Select(attrs={'class': 'selectEstado'}, choices=ESTADO_CHOICES),
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


class DateSelector(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            # Check if the end date is before the start date
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

            # Check if the start date or end date is in the future
            if fecha_inicio >= date.today() or fecha_fin > date.today():
                raise forms.ValidationError('La fecha de inicio/fin no puede ser una fecha futura.')
        
        return cleaned_data
    
    
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