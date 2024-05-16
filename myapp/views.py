from django.http import HttpResponse, JsonResponse
from .models import Project, Sucursal, intercambios
from django.shortcuts import render, redirect
from .forms import crear_intercambio_con_espera_de_ofertas
from django.contrib import messages

# Create your views here.


def index(request):
    title = 'Django Course!!'
    return render(request, 'index.html', {
        'title': title
    })


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





def Sucursales(request):
    # projects = list(Project.objects.values())
    sucurs = Sucursal.objects.all()

    return render(request, 'Sucursales.html',{'sucursales' : sucurs})
    

def eliminar_sucursal(request, sucursal_id):
    sucursal = Sucursal.objects.get(id=sucursal_id)
    sucursal.delete()
    return redirect('Sucursales')



def editar_sucursal(request, sucursal_id):
    if request.method == 'POST':
        nueva_direccion = request.POST.get('NuevaDireccion')
        sucursal = Sucursal.objects.get(id=sucursal_id)
        sucursal.title = nueva_direccion
        sucursal.save()
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
    projectos = Project.objects.all()
    context = {'title': title, 'projectos': projectos}
    return render(request, 'Mis_Trueques.html', context)

def Crear_Trueque(request):
    title = 'Mis trueques'
    context = {'title': title}
    return render(request, 'Crear_Trueques.html', context)

def Menu_Sucursales(request):
    title = 'Menu de Sucursales'
    context = {'title': title}
    return render(request, 'Menu_Sucursales.html', context)

def intercambio_con_espera_de_ofertas(request):
    if request.method == 'POST':
        # guardar foto en la carpeta
        # guardar en la base de datos la ubicacion de la foto.
        # que pasa cuando dos usuarios cargan una imagen con el mismo nombre? guardar con nombrusuario mas el nombre de la foto y si se repite se incrementa en 1 nombrefoto
        intercambio = intercambios.objects.create(
        nombre = request.POST['nombre'],
        estado = request.POST['estado'],
        categoria = request.POST['categoria'],
        foto = request.FILES['foto'],
        descripcion = request.POST['descripcion'],
        modelo = request.POST['modelo'],
        marca = request.POST['marca']
        ) 
        messages.success(request,"intercambio creado correctamente")
        return redirect('intercambio_con_espera_de_ofertas')
    title = 'intercambio con espera de ofertas'
    context = {'title': title, 'form' : crear_intercambio_con_espera_de_ofertas()}
    return render(request, 'intercambio_con_espera_de_ofertas.html', context)

