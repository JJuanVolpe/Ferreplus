from django import forms


    

class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del Proyect", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))


class RecoveryForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', required=True, max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Introduzca su email'}))
class PopupForm(forms.Form):
    message = forms.CharField(label='Mensaje del Popup', max_length=100)
