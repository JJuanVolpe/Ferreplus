from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('index/', views.index, name="index"),
    path('signup/', views.signup, name='signup'),    
    path('', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('menuPrincipal/', views.menuPrincipal, name = "menuPrincipal"),
    path('miPerfil/', views.miPerfil, name = "miPefil"),
    path('sucursales/',views.Sucursales,name='Sucursales'),
    path('verSucursales/',views.verSucursales,name="verSucursales"),
    path('intercambio_con_espera_de_ofertas/',views.intercambio_con_espera_de_ofertas,name="intercambio_con_espera_de_ofertas"),
    path('intercambios/',views.Menu_intercambios,name="Menu_De_Intercambios"),
    path('historial-intercambios/',views.Historial_Intercambios, name="Historial_De_Intercambios"),
    path('create-trade/<int:trueque_id>/', views.create_trade, name='create_trade'),
    path('mis-intercambios/',views.Ver_trueques, name="Mis_Trueques"),
    path('ver_objetos_postulados/<int:trueque_id>',views.ver_objetos_postulados, name="ver_objetos_postulados"),
    path('menu-sucursales/',views.Menu_Sucursales, name="Menu_Sucursales"),
    path('eliminar_sucursal/<int:sucursal_id>/', views.eliminar_sucursal, name='eliminar_sucursal'),
    path('editar_sucursal/<int:sucursal_id>/', views.editar_sucursal, name='editar_sucursal'),
    path('agregar_sucursal/', views.agregar_sucursal, name='agregar_sucursal'),
    path('menuEmpleado/', views.menu_empleado, name="menuEmpleado"),
    path('gestionarEmpleados/', views.gestionarEmpleados,name="gestionarEmpleados"),
    path('editarEmpleados/<int:empleado_id>', views.editarEmpleado, name="editar_empleado" ),
    path('eliminar_empleado/<int:user_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('filtrar/', views.filtrar_productos_por_filtro, name='filtrar_productos_por_filtro'),
    path('aceptar_trueque/<int:obj_id>/', views.aceptar_trueque, name='aceptar_trueque'),
    path('rechazar_trueque/<int:obj_id>/', views.rechazar_trueque, name='rechazar_trueque'),
    path('cancelar_trueque/<int:trueque_id>/', views.cancelar_trueque, name='cancelar_trueque'),
    path('intercambiosaceptados/<int:intercambio_id>', views.historialaceptados,name='intercambiosaceptados'),
    path('intercambiosaceptados/', views.historialaceptados, name='intercambiosaceptados'),
    path('rate/<int:intercambio_id>/', views.rate_profile, name='rate_profile'),
    path('rate/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('verEstadisticas/', views.ver_estadisticas,name="verEstadisticas")
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)