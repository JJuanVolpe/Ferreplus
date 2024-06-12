from itertools import groupby
import random
import string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import Error, IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Profile, Rating, Sucursal, intercambios, Product
from .forms import RecoveryForm, crear_intercambio_con_espera_de_ofertas, ProductForm
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from datetime import time,datetime
from django.db.models import Avg

import re  # Importación del módulo r


# Create your views here.


def index(request):
    title = 'Django Course!!'
    return render(request, 'index.html', {
        'title': title
    })


def menuPrincipal(request):
    return render(request, 'menuPrincipal.html')


def miPerfil(request):
    previous_page = request.META.get('HTTP_REFERER')
    usuario = request.user  # Obtenemos el usuario autenticado
    


    if request.method == 'POST':
        if 'contraseñaActual' in request.POST:
            # El formulario se envió desde el modal de cambio de contraseña
            contraseña_actual = request.POST.get('contraseñaActual')
            nueva_contraseña = request.POST.get('contraseñaNueva')
            repetir_nueva_contraseña = request.POST.get('repetirContraseñaNueva')

            # Verificar si la contraseña actual coincide con la del usuario
            if usuario.check_password(contraseña_actual):
                if contraseña_actual == nueva_contraseña:
                    messages.error(request, 'La nueva contraseña no puede ser igual a la actual.')
                else:
                    # Validar la nueva contraseña con los requisitos específicos
                    if len(nueva_contraseña) < 8:
                        messages.error(request, 'La nueva contraseña debe tener al menos una letra mayúscula y al menos 8 caracteres.')
                    elif not re.search(r'[A-Z]', nueva_contraseña):
                        messages.error(request, 'La nueva contraseña debe tener al menos una letra mayúscula y al menos 8 caracteres.')
                    else:
                        if nueva_contraseña == repetir_nueva_contraseña:
                            # Actualizar la contraseña del usuario
                            usuario.set_password(nueva_contraseña)
                            usuario.save()
                            update_session_auth_hash(request, usuario)  # Mantener la sesión activa
                            messages.success(request, 'La contraseña se ha actualizado correctamente.')
                        else:
                            messages.error(request, 'Las nuevas contraseñas no coinciden.')
            else:
                messages.error(request, 'La contraseña actual es incorrecta.')
        else:
            # El formulario se envió desde el botón "Guardar cambios" fuera del modal
            try:
                edad = int(request.POST['edad'])
                if edad < 18:
                    messages.error(request, 'La edad debe ser mayor o igual a 18 años.')
                else:
                    usuario.profile.telefono = request.POST['telefono']
                    usuario.profile.genero = request.POST['genero']
                    usuario.profile.edad = edad
                    usuario.username = request.POST['username']
                    usuario.email = request.POST['email']
                    usuario.first_name = request.POST['first_name']
                    usuario.last_name = request.POST['last_name']
                    usuario.save()  # Guardar los cambios en la base de datos
                    messages.success(request, 'Los cambios se han guardado correctamente.')
            except ValueError:
                messages.error(request, 'Por favor, ingrese una edad válida.')

    return render(request, 'miPerfil.html', {
        'previous_page': previous_page, 
        'usuario': usuario}
    )

@login_required
def intercambio_con_espera_de_ofertas(request):
    if request.method == 'POST':
        intercambios.objects.create(
            nombre=request.POST['nombre'],
            estado=request.POST['estado'],
            categoria=request.POST['categoria'],
            foto=request.FILES['foto'],
            descripcion=request.POST['descripcion'],
            modelo=request.POST['modelo'],
            marca=request.POST['marca'],
            sucursal_asignada = get_object_or_404(Sucursal, id=request.POST['sucursal']),
            usuario=request.user.profile,
        )
        # Agrega un mensaje de éxito
        messages.success(request, "El intercambio se ha creado correctamente.")
        # Redirige a la página de Mis_Trueques
        return redirect('Mis_Trueques')
    else:
        
        title = 'intercambio con espera de ofertas'
        context = {'title': title, 'form': crear_intercambio_con_espera_de_ofertas(), 'sucursales': Sucursal.objects.all()}
        return render(request, 'intercambio_con_espera_de_ofertas.html', context)
    
def incorrect_password(password):
        if len(password) < 8:
            return True
        else:
            for i in password:
                if (not i.isdigit() and i.isupper()):   #no es un número y es mayuscula? cumple
                    return False
        return True
        
def signup(request):
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
            user.profile.genero = request.POST['genero']
            user.profile.telefono = request.POST["telefono"]
            user.save()
            login(request, user)
            return redirect('/')
        except IntegrityError:  #Manejo error asociado a la BD 
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "Nombre de usuario ya existente en el sistema."})



def signin(request):
    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirige según su perfil
        profile = Profile.objects.get(user=request.user)
        if profile.es_gerente:
            return redirect('Sucursales')
        elif profile.es_empleado:
            return redirect('menuEmpleado') 
        else:
             return redirect('menuPrincipal')

    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Accede al perfil del usuario
            profile = Profile.objects.get(user=user)
            if profile.es_gerente:  # Verifica si el usuario es gerente
                return redirect('Sucursales')
            elif profile.es_empleado:
                return redirect('menuEmpleado')
            else:    
                return redirect('menuPrincipal')
        else:
            # Verifica si el error fue debido a un nombre de usuario no válido o contraseña incorrecta
            try:
                user = Profile.objects.get(user__username=username)
                error_message = "Contraseña incorrecta"
            except Profile.DoesNotExist:
                error_message = "Nombre de usuario no se encuentra registrado"
                
            return render(request, 'signin.html', {"form": AuthenticationForm(), "error": error_message})

def editarEmpleado(request,empleado_id):
    empleado = Profile.objects.get(id=empleado_id)
    sucursales = Sucursal.objects.all()
    if 'guardarEdicion' in request.POST:
        empleado.user.first_name = request.POST.get('first_name')
        empleado.user.last_name = request.POST.get('last_name')
        empleado.edad = request.POST["edad"]
        empleado.dni = request.POST["dni"]
        empleado.genero = request.POST['genero']
        empleado.telefono = request.POST["telefono"]
        empleado.sucursal = Sucursal.objects.get(id=request.POST["sucursal"])
        empleado.user.save()
        empleado.save()
        messages.success(request, "Empleado Editado Exitosamente")
        return redirect('gestionarEmpleados')
    return render(request, 'editarEmpleado.html',{"empleado":empleado,
                                                "sucursales":sucursales})
    
def eliminar_empleado(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, "Empleado eliminado exitosamente.")
    return redirect('gestionarEmpleados')   

def gestionarEmpleados(request):
    if 'guardarEmpleado' in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contraseña =  request.POST.get('contraseña')
        # Validar la nueva contraseña con los requisitos específicos
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
        elif len(contraseña) < 8:
            messages.error(request, 'La contraseña debe tener al menos una letra mayúscula y al menos 8 caracteres.')
        elif not re.search(r'[A-Z]', contraseña):
            messages.error(request, 'La contraseña debe tener al menos una letra mayúscula y al menos 8 caracteres.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
        else:
            user = User.objects.create_user(username=username, email=email, first_name=first_name, 
                                            last_name=last_name, password=contraseña)
            user.profile.edad = request.POST["edad"]
            user.profile.dni = request.POST["dni"]
            user.profile.genero = request.POST['genero']
            user.profile.telefono = request.POST["telefono"]
            user.profile.es_empleado = True
            user.profile.sucursal = Sucursal.objects.get(id=request.POST["sucursal"])
            user.save()
            messages.success(request, "Usuario creado exitosamente.")

    # Manejar la obtención de empleados
    empleados = Profile.objects.filter(es_empleado=True)
    sucursales = Sucursal.objects.all()
    return render(request, 'Empleados.html', {'empleados': empleados,
                                              "sucursales": sucursales})

@login_required
def signout(request):
    logout(request)
    return redirect('/')



def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html', {'form': RecoveryForm()})
    else:
        # Deberia trabajarlo con formularios => contact_form = RecoveryForm(data=request.POST)
        account_email = request.POST["email"]
        try:
            new_password = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
            if User.objects.filter(email=account_email).exists():
                user = User.objects.get(email=account_email)
                user.set_password(new_password)
            else:
                raise Error("No existe usuario con ese correo asociado")
            # Enviar el correo electrónico
            email = EmailMessage('Mensaje de recuperación de contraseña - Ferreplus 🛠️🧰','{} \n- Su nueva contraseña es: \n\n{}'
                .format("No compartas esta información, nadie de nuestro equipo te la solicitará.", new_password),
                account_email, ['da79fcc5174cf2@inbox.mailtrap.io'])
            email.send()
            user.save()
            return redirect(reverse('contact')+'?ok')   #Todo OK
        except:
            # Ha habido un error y retorno a ERROR
            return redirect(reverse('contact')+'?error')
        
        
@login_required
def Sucursales(request):
    profile = Profile.objects.get(user=request.user)  # Obtener el perfil del usuario actual
    if not profile.es_gerente:
        # Si el usuario no es gerente, mostrar un mensaje de error
        return render(request, 'Sucursales.html', {'error': 'No tienes permisos para acceder a esta página.'})
    
    # Si el usuario es gerente, obtener todas las sucursales
    sucursales = Sucursal.objects.all()
    return render(request, 'Sucursales.html', {'sucursales': sucursales})

  
def Ver_trueques(request):
    # Obtener la lista de intercambios del usuario
    usuario = request.user
    trueques = intercambios.objects.filter(usuario=usuario.profile, status='NUEVO')
    
    # Pasar tanto la lista de intercambios como el path absoluto al contexto
    context = {
        'listadointercambios': trueques,
    }
    if 'eliminar' in request.POST:
        # Acción para eliminar el trueque
        trueque = intercambios.objects.get(id=request.POST['trueque_id'])
        trueque.delete()
        messages.success(request, '¡El intercambio se ha eliminado correctamente!')
        return redirect('Mis_Trueques')
    elif request.method == 'POST':
        trueque = intercambios.objects.get(id=request.POST['trueque_id'])
        trueque.categoria= request.POST['categoria']
        trueque.descripcion= request.POST['descripcion']
        trueque.marca= request.POST['marca']
        trueque.estado= request.POST['estado']
        trueque.nombre= request.POST['nombre']
        trueque.modelo= request.POST['modelo']
        # Si se proporciona una foto, asignarla al campo 'foto' del trueque
        if 'foto' in request.FILES:
            trueque.foto = request.FILES['foto']
        trueque.save()
    
    return render(request, 'Mis_Trueques.html', context)

def eliminar_sucursal(request, sucursal_id):
    sucursal = Sucursal.objects.get(id=sucursal_id)
    sucursal.delete()
    messages.success(request, '¡La sucursal se ha eliminado correctamente!')
    return redirect('Sucursales')

def editar_sucursal(request, sucursal_id):
    if request.method == 'POST':
        nueva_direccion = request.POST.get('address')
        nueva_ciudad = request.POST.get('city')
        sucursal = Sucursal.objects.get(id=sucursal_id)
        if sucursal.address == nueva_direccion and sucursal.city == nueva_ciudad:
             messages.error(request, ' Se ingresaron los mismos datos que ya posee la sucursal')
        elif not Sucursal.objects.filter(address=nueva_direccion, city=nueva_ciudad).exists():
            sucursal.address = nueva_direccion
            sucursal.city = nueva_ciudad
            sucursal.save()
            messages.success(request,"¡La sucursal se editó exitosamente!")
        else:
            messages.error(request, '¡La direccion y ciudad que se quiere ingresar ya pertenece a otra sucursal!')
    return redirect('Sucursales')

def agregar_sucursal(request):
    if request.method == 'POST':
        nueva_sucursal = request.POST.get('nuevaSucursal')
        nueva_ciudad = request.POST.get('nueva_ciudad')
        if not Sucursal.objects.filter(address=nueva_sucursal, city=nueva_ciudad).exists():
            Sucursal.objects.create(address=nueva_sucursal, city= nueva_ciudad)
            messages.success(request,'¡La sucursal se agrego correctamente!')
        else:
                
            messages.error(request, '¡La direccion que se quiere ingresar ya pertenece a otra sucursal de la misma ciudad!')
    return redirect('Sucursales')


def verSucursales(request):
    sucursales = Sucursal.objects.all()
    return render(request,'verSucursales.html',{
        'sucursales':sucursales
    })


def Menu_intercambios(request):
    title = 'Menu Intercambio'
    trueques = intercambios.objects.filter(status='NUEVO')
    context = {'title': title,
               'trueques':trueques,
                'form': ProductForm()}
    return render(request, 'Menu_De_Intercambios.html', context)


def Historial_Intercambios(request):
    title = 'Historial de intercambios'
    trueques = intercambios.objects.order_by('status')
    trueque_data = {
        status: list(items) 
        for status, items in groupby(trueques, key=lambda x: x.status)
    }
    
    trueques_realizados = []
    trueques_cancelados = []
    #trueques_pendientes = trueque_data.get("PENDIENTE", [])
    
    valorables_ids = []
    for intercambio in trueques_realizados:
        prod_by_postuler = get_object_or_404(Product, trueque_postulado=intercambio)
        if request.user.profile == intercambio.usuario or prod_by_postuler.postulante == request.user.profile:
            trueques_realizados.append(intercambio)
            if can_rate(request.user.profile, prod_by_postuler.trueque_postulado):
                valorables_ids.append(intercambio.id)
    
    for intercambio in trueques.filter(status='CANCELADO'):
        prod_by_postuler = get_object_or_404(Product, trueque_postulado=intercambio)
        if request.user.profile == intercambio.usuario or prod_by_postuler.postulante == request.user.profile:
            trueques_cancelados.append(intercambio)
    
    trueques_pendientes = intercambios.objects.filter(usuario=request.user.profile).get("PENDIENTE", [])
    
    
    context = {
        'title': title,
        'trueques_pendientes': trueques_pendientes,
        'trueques_realizados': trueques_realizados,
        'trueques_cancelados': trueques_cancelados,
        'valorables_ids': valorables_ids
        
    }
    return render(request, 'Historial_De_Intercambios.html', context)

def create_trade(request, trueque_id):
    if request.method == 'POST':
        trueque = get_object_or_404(intercambios, id=trueque_id)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form_category = form.cleaned_data['categoria']
            if form.cleaned_data['fecha']<= datetime.today().date():
               messages.error(request,'La fecha debe ser mayor a la fecha actual')
            elif form.cleaned_data['hora']< time(8, 0) or form.cleaned_data['hora']> time(20, 0):
                messages.error(request,'La hora debe ser mayor a las 08:00 y menor a las 20:00')
            elif form_category != trueque.categoria:
                messages.error(request, 'La categoria del objeto ingresado debe corresponderse con la del objeto a intercambiar.')
            elif request.user == trueque.usuario.user: # No debo dejar que un usuario postule a un trueque de el mismo
                messages.error(request, 'No puede postular un objeto para un trueque creado por usted.')
            else:
                Product.objects.create(hora=form.cleaned_data['hora'], fecha=form.cleaned_data['fecha'], nombre=form.cleaned_data['nombre'], estado=form.cleaned_data['estado'],
                                       categoria=form.cleaned_data['categoria'], foto=form.cleaned_data['foto'],
                                       marca=form.cleaned_data['marca'],modelo=form.cleaned_data['modelo'],
                                       descripcion=form.cleaned_data['descripcion'], postulante=request.user.profile,
                                       trueque_postulado=trueque)
                
                #form.save()
                messages.success(request, 'El objeto ha sido creado y postulado con éxito.')
                #Aquí se debe enviar mail al usuario de que se generó postulación al trueque que hizo?
    return Menu_intercambios(request=request)

def ver_objetos_postulados(request, trueque_id):

    trueque = get_object_or_404(intercambios, id=trueque_id)
    title = 'Listado ofrecido para intercambiar objeto:' +  trueque.nombre + ', marca: ' + trueque.marca
    trueques = intercambios.objects
    objetos_postulados = Product.objects.filter(trueque_postulado=trueque)
    context = {
        'title': title,
        'objetos_postulados': objetos_postulados, 
    }
    
    return render(request, 'ver_objetos_postulados.html', context)

def Crear_Trueque(request):
    title = 'Mis trueques'
    context = {'title': title}
    return render(request, 'Crear_Trueques.html', context)

def Menu_Sucursales(request):
    title = 'Menu de Sucursales'
    context = {'sucursales': Sucursal.objects.all()}
    return render(request, 'Menu_Sucursales.html', context)

def menu_empleado(request):
    usuario = request.user.profile
    suc = usuario.sucursal
    intercambiossuc = intercambios.objects.filter(sucursal_asignada=suc, status="PENDIENTE")
    if request.method == 'POST':
        return redirect('intercambiosaceptados')
    intercambiossuc = intercambios.objects.filter(sucursal_asignada=suc, status="PENDIENTE")
    if request.method == 'POST':
        return redirect('intercambiosaceptados')

    context = {'sucursal': suc, 'intercambios': intercambiossuc}
    return render(request, 'menuEmpleado.html', context)
    context = {'sucursal': suc, 'intercambios': intercambiossuc}
    return render(request, 'menuEmpleado.html', context)

def historialaceptados(request, intercambio_id=None):
    if intercambio_id:
        intercambio = get_object_or_404(intercambios, id=intercambio_id)
        intercambio.status = "REALIZADO"
        intercambio.save()
    usuario = request.user.profile
    suc = usuario.sucursal
    aceptados = intercambios.objects.filter(sucursal_asignada=suc, status="REALIZADO")
    context = {'aceptados': aceptados}
    return render(request, 'historialaceptados.html', context)


def filtrar_productos_por_filtro(request):
        query = request.GET.get('search_query')
        search_type = request.GET.get('search_type', 'estado')  # Por defecto, busca por estado
        if query:
            if search_type == 'estado':
                productos = intercambios.objects.filter(estado__icontains=query)
            elif search_type == 'sucursal':
                # Obtener la sucursal que cumple con la consulta
                chars = query.lower()
                newlist = [x for x in Sucursal.objects.all() if chars in x.address.lower() or chars in x.city.lower()]
                productos = [obj for obj in intercambios.objects.all() if obj.sucursal_asignada in newlist]
            if  not productos:
                messages.error(request, 'No existen objetos con el estado o sucursal ingresado.')
                productos = intercambios.objects.filter(status="NUEVO").all()
        else:
            messages.error(request, 'No se proporcionó ninguna cadena para buscar.')
            productos = intercambios.objects.filter(status="NUEVO").all()
        return render(request, 'Menu_De_Intercambios.html', {'trueques': productos, 'form': ProductForm()})


def aceptar_trueque(request, obj_id):
        postuled =  get_object_or_404(Product, id=obj_id)
        for offer in Product.objects.filter(trueque_postulado=postuled.trueque_postulado):
            #Elimina el resto de obj. postulados
            if offer != postuled:
                offer.delete()
            
        trueque = postuled.trueque_postulado
        trueque.status = 'PENDIENTE'
        
        trueque.save()
        #Falta el código pa hacer algo con los obj. postulados restantes. 
        return Historial_Intercambios(request)


def rechazar_trueque(request, obj_id):
        postuled =  Product.objects.filter(id=obj_id)
        trueque_id = postuled.trueque_postulado.id

        postuled.delete()
        
        return ver_objetos_postulados(request, trueque_id=trueque_id)

def cancelar_trueque(request, trueque_id):
        trueque = get_object_or_404(intercambios, id=trueque_id)
        trueque.status = 'CANCELADO'
        postulados = Product.objects.filter(trueque_postulado=trueque)
        for obj in postulados:
            obj.delete()
        
        trueque.save()
        if request.user.profile.es_empleado:
            return menu_empleado(request)

        return Historial_Intercambios(request)



def can_rate(profile, intercambio):
    return (profile.es_empleado and not intercambio.valoradoEmpleado) or \
            (profile == intercambio.usuario and not intercambio.valoradoPostulante) or \
            (profile != intercambio.usuario and not intercambio.valoradoUsuario)
            

def rate_profile(request, intercambio_id):
    intercambio = get_object_or_404(intercambios, id=intercambio_id)
    profile = intercambio.usuario #Percibo que quién valora es el postulante (justamente al creador del trade)
    user_actual = request.user.profile
    if profile == user_actual:
        profile = get_object_or_404(Product, trueque_postulado=intercambio).postulante
    context = {
        'actual_user': user_actual,
        'profile': profile,
        'intercambio' : intercambio,
        'puede_valorar' : can_rate(user_actual, intercambio)
    }
    if request.method == "POST":
        if not request.POST.get('rating'):
            return render(request, 'rate_profile.html', context=context)
        
        rating_value = int(request.POST.get('rating', 0)) # Obtener o crear la instancia de Rating       
        if (user_actual == intercambio.usuario): #Si soy el creador del trueque voto al postulante
            intercambio.valoradoPostulante = True 
        elif user_actual.es_empleado:
            intercambio.valoradoEmpleado = True 
        elif not intercambio.valoradoUsuario:
            intercambio.valoradoUsuario = True #El usuario valora al creador de trueque
        intercambio.save()
        rating_obj, created = Rating.objects.get_or_create(profile=profile, defaults={'rating': rating_value})
        if not created: # Si ya existe, actualizar la valoración sumando la nueva
            rating_obj.rating += rating_value
            rating_obj.cantValoraciones += 1
            rating_obj.save()
        redirect_url = '/historial-intercambios/'
        if user_actual.es_empleado:
            redirect_url = '/menuEmpleado'
        return JsonResponse({'success': True, 'redirect_url': redirect_url})
    else:
        return render(request, 'rate_profile.html', context=context)
        




def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    average_rating = profile.ratings.aggregate(Avg('rating'))['rating__avg']

    context = {
        'profile': profile,
        'average_rating': average_rating,
        'usuario': profile.user,
    }
    return render(request, 'miPerfil.html', context)
