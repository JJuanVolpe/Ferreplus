from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Profile, Project, Sucursal
from .forms import CreateNewProject, RecoveryForm
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.


def index(request):
    title = 'Django Course!!'
    return render(request, 'index.html', {
        'title': title
    })


def menuPrincipal(request):
    return render(request, 'menuPrincipal.html')

def  miPerfil(request):
    previous_page = request.META.get('HTTP_REFERER')
    usuario = request.user    # Obtenemos el usuario autenticado
    #usuario = User.objects.all()[3]
    if request.method == 'POST':
        if 'contraseñaActual' in request.POST:
            # El formulario se envió desde el modal de cambio de contraseña
            contraseña_actual = request.POST.get('contraseñaActual')
            nueva_contraseña = request.POST.get('contraseñaNueva')
            repetir_nueva_contraseña = request.POST.get('repetirContraseñaNueva')
            
            # Verificar si la contraseña actual coincide con la del usuario
            if usuario.check_password(contraseña_actual):
                try:
                    validate_password(nueva_contraseña, user=usuario)
                except ValidationError as error:
                    messages.error(request, error.messages[0])
                else:  # Solo si la validación de la contraseña pasa sin excepciones
                    if nueva_contraseña == repetir_nueva_contraseña:
                        # Actualizar la contraseña del usuario
                        usuario.set_password(nueva_contraseña)
                        usuario.save()
                        messages.success(request, 'La contraseña se ha actualizado correctamente.')
                    else:
                        messages.error(request, 'Las nuevas contraseñas no coinciden.')
            else:
                messages.error(request, 'La contraseña actual es incorrecta.')
        else:
            # El formulario se envió desde el botón "Guardar cambios" fuera del modal
            usuario.profile.telefono = request.POST['telefono']
            usuario.profile.genero = request.POST['genero']
            usuario.profile.edad = request.POST['edad']
            usuario.username = request.POST['username']
            usuario.email = request.POST['email']
            usuario.first_name = request.POST['first_name']
            usuario.last_name = request.POST['last_name']
            usuario.save()  # Guardar los cambios en la base de datos
            messages.success(request, 'Los cambios se han guardado correctamente.')
    return render(request, 'miPerfil.html', {
        'previous_page': previous_page, 
        'usuario': usuario}
    )




def signup(request):
    def incorrect_password(password):
        if len(password) < 8:
            return True
        else:
            for i in password:
                if (not i.isdigit() and i.isupper()):   #no es un número y es mayuscula? cumple
                    return False
        return True
    
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        if User.objects.filter(email=request.POST["email"]).exists():
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "Este correo está en uso, debe utilizar otro."})
        if incorrect_password(request.POST["password"]):
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "La contraseña debe tener mínimo 8 dígitos y una mayúscula."})
        if int(request.POST["edad"]) < 18:
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "Debe ser mayor de edad para registarse."})
        try:
            user = User.objects.create_user(
                request.POST["username"], password=request.POST["password"],
                email=request.POST["email"],  first_name=request.POST["name"],
                last_name=request.POST["lastname"])
            user.profile.edad = request.POST["edad"]
            user.profile.dni = request.POST["dni"]
            user.profile.genero = request.POST["genero"]
            user.profile.telefono = request.POST["telefono"]
            user.save()
            login(request, user)
            return redirect('')
        except IntegrityError:  #Manejo error asociado a la BD 
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "Nombre de usuario ya existente en el sistema."})


def signin(request):
    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirige según su perfil
        profile = Profile.objects.get(user=request.user)
        if profile.Es_gerente:
            return redirect('Sucursales')
        else:
            return redirect('menuPrincipal')

    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm(), "error": "Nombre de usuario o contraseña incorrecto"})
        else:
            login(request, user)
            # Accede al perfil del usuario
            profile = Profile.objects.get(user=user)
            if profile.Es_gerente:  # Verifica si el usuario es gerente
                return redirect('Sucursales')
            else:    
                return redirect('menuPrincipal')

@login_required
def signout(request):
    logout(request)
    return redirect('signin')


def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': RecoveryForm()})
    else:
        # Deberia trabajarlo con formularios => contact_form = RecoveryForm(data=request.POST)
        account_email = request.POST["email"]
        try:
            password = "password"
            if User.objects.filter(email=account_email).exists():
                user = User.objects.get(email=account_email)
                user.set_password("password")
            # Enviar el correo electrónico
            email = EmailMessage('Mensaje de recuperación de contraseña - Ferreplus 🛠️🧰','{} \n- Su nueva contraseña es: \n\n{}'
                .format("No compartas esta información, nadie de nuestro equipo te la solicitará.", password),
                account_email, ['808a2280ba84f8@inbox.mailtrap.io'])
            email.send()
            user.save()
            return redirect(reverse('contact')+'?ok')   #Todo OK
        except:
            # Ha habido un error y retorno a ERROR
            return redirect(reverse('contact')+'?error')
        

def Sucursales(request):
    profile = Profile.objects.get(user=request.user)  # Obtener el perfil del usuario actual
    if not profile.Es_gerente:
        # Si el usuario no es gerente, mostrar un mensaje de error
        return render(request, 'Sucursales.html', {'error': 'No tienes permisos para acceder a esta página.'})
    
    # Si el usuario es gerente, obtener todas las sucursales
    sucursales = Sucursal.objects.all()
    return render(request, 'Sucursales.html', {'sucursales': sucursales})
    

def eliminar_sucursal(request, sucursal_id):
    sucursal = Sucursal.objects.get(id=sucursal_id)
    sucursal.delete()
    return redirect('Sucursales')



def editar_sucursal(request, sucursal_id):
    if request.method == 'POST':
        nueva_direccion = request.POST.get('NuevaDireccion')
        if len(nueva_direccion)<35:
            if not Sucursal.objects.filter(title= nueva_direccion).exists():
                sucursal = Sucursal.objects.get(id=sucursal_id)
                sucursal.title = nueva_direccion
                sucursal.save()
            else:
                messages.error(request, '¡La direccion que se quiere ingresar ya pertenece a otra sucursal!')
        else: 
            messages.error(request, '¡El campo de la direccion no se puede exceder de los 35 caracteres!')
    return redirect('Sucursales')


def agregar_sucursal(request):
    if request.method == 'POST':
        nueva_sucursal = request.POST.get('nuevaSucursal')
        if len(nueva_sucursal)<35:
            if not Sucursal.objects.filter(title= nueva_sucursal).exists():
                Sucursal.objects.create(title=nueva_sucursal)
            else:
                    
                messages.error(request, '¡La direccion que se quiere ingresar ya pertenece a otra sucursal!')
        else: 
            messages.error(request, '¡El campo de la direccion no se puede exceder de los 35 caracteres!')
    return redirect('Sucursales')


def Menu_intercambios(request):
    title = 'Menu Intercambio'
    context = {'title': title}
    return render(request, 'Menu_De_Intercambios.html', context)

def Historial_Intercambios(request):
    title = 'Historial de intercambios'
    context = {'title': title}
    return render(request, 'Historial_De_Intercambios.html', context)

def Ver_Trueques(request):
    title = 'Mis trueques'
    context = {'title': title}
    return render(request, 'Mis_Trueques.html', context)

def Crear_Trueque(request):
    title = 'Mis trueques'
    context = {'title': title}
    return render(request, 'Crear_Trueques.html', context)

def Menu_Sucursales(request):
    title = 'Menu de Sucursales'
    context = {'title': title}
    return render(request, 'Menu_Sucursales.html', context)