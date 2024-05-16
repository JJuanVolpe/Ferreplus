from django import forms 

class crear_intercambio_con_espera_de_ofertas(forms.Form):
    nombre = forms.CharField(label="nombre",max_length=200)
    estado = forms.CharField(label="estado",max_length=200)
    categoria = forms.CharField(label="categoria",max_length=200)
    foto = forms.ImageField()
    descripcion = forms.CharField(label="descripcion",max_length=200)
    modelo = forms.CharField(label="modelo",max_length=200)
    marca = forms.CharField(label="marca",max_length=200)
    