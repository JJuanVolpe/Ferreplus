from django import forms

class CreateNewTask(forms.Form):
    title = forms.CharField(label="Titulo de tarea", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    description=forms.CharField(label="descripcion de la tarea", widget=forms.Textarea(attrs={'class': 'input'}))
    

class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del Proyect", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))


class RecoveryForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', required=True, max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Introduzca su email'}))
