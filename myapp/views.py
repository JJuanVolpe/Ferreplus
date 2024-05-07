from django.http import HttpResponse
from .models import Project, Task
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateNewTask, CreateNewProject
from django.contrib.auth.models import User
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
    #usuario = request.user  # Obtenemos el usuario autenticado
    usuario = User.objects.all()[3]
  
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


def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask()
        })
    else:
        Task.objects.create(
            title=request.POST['title'], description=request.POST['description'], project_id=2)
        return redirect('tasks')


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