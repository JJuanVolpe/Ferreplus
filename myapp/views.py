from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Task, Profile, Project, Task
from .forms import CreateNewTask, CreateNewProject, RecoveryForm
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

def about(request):
    username = 'fazt'
    return render(request, 'about.html', {
        'username': username
    })


def hello(request, username):
    return HttpResponse("<h2>Hello %s</h2>" % username)


def projects(request):
    # projects = list(Project.objects.values())
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {
        'projects': projects
    })


def tasks(request):
    # task = Task.objects.get(title=tile)
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

    
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})
        #Task.objects.create(
        #    title=request.POST['title'], description=request.POST['description'], project_id=2)
        #return redirect('tasks')


def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(name=request.POST["name"])
        return redirect('projects')

def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks
    })


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
            return redirect('menuPrincipal')
        except IntegrityError:  #Manejo error asociado a la BD 
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})



def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})
        login(request, user)
        return redirect('menuPrincipal')
        return redirect('menuPrincipal')


@login_required
def signout(request):
    logout(request)
    return redirect('index')


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
        
