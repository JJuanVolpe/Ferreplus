from django.http import HttpResponse, JsonResponse
from .models import Project, Sucursal
from django.shortcuts import render, redirect, get_object_or_404


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


def agregar_sucursal(request):
    if request.method == 'POST':
        nueva_sucursal = request.POST.get('nuevaSucursal')
        if nueva_sucursal:
            sucursal = Sucursal.objects.create(title=nueva_sucursal)
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

