from django import forms


class crear_intercambio_con_espera_de_ofertas(forms.Form):
    nombre = forms.CharField(label="nombre",max_length=200)
    estado = forms.CharField(label="estado",max_length=200)
    categoria = forms.CharField(label="categoria",max_length=200)
    foto = forms.ImageField()
    descripcion = forms.CharField(label="descripcion",max_length=200)
    modelo = forms.CharField(label="modelo",max_length=200)
    marca = forms.CharField(label="marca",max_length=200)
    

class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del Proyect", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))


class RecoveryForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', required=True, max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Introduzca el correo asociado a una cuenta existente', 'autocomplete':'on'}))


class PopupForm(forms.Form):
    message = forms.CharField(label='Mensaje del Popup', max_length=100)
