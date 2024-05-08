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


    def ModificarSucursal(request, id_buscado):
        if request.method == 'POST':
            direcc = request.POST.get('direccNueva')
            sucur = Sucursal.objects.get(id=id_buscado)
            sucur.title = direcc
            sucur.save()
            return redirect('Sucursales.html',{'sucursales' : Sucursal.objects.all()})  # Redirige a la lista de sucursales





    return render(request, 'Sucursales.html',{'sucursales' : sucurs})
    








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

