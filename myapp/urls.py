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
    path('menu_principal/', views.menu_principal, name = "menu_principal"),
    path('profile/', views.user_perfil, name = "user_perfil"),
    path('gestionar_sucursales/',views.gestionar_sucursales,name='gestionar_sucursales'),
    path('sucursales_disponibles/',views.ver_sucursales,name="ver_sucursales"),
    path('intercambio_con_espera_de_ofertas/',views.intercambio_con_espera_de_ofertas,name="intercambio_con_espera_de_ofertas"),
    path('intercambios/',views.menu_intercambios,name="menu_de_intercambios"),
    path('historial_intercambios/',views.historial_intercambios, name="historial_de_intercambios"),
    path('create-trade/<int:trueque_id>/', views.create_trade, name='create_trade'),
    path('mis-intercambios/',views.ver_trueques, name="mis_trueques"),
    path('ver_objetos_postulados/<int:trueque_id>',views.ver_objetos_postulados, name="ver_objetos_postulados"),
    path('menu_sucursales/',views.menu_sucursales, name="menu_sucursales"),
    path('eliminar_sucursal/<int:sucursal_id>/', views.eliminar_sucursal, name='eliminar_sucursal'),
    path('editar_sucursal/<int:sucursal_id>/', views.editar_sucursal, name='editar_sucursal'),
    path('agregar_sucursal/', views.agregar_sucursal, name='agregar_sucursal'),
    path('menu_empleado/', views.menu_empleado, name="menu_empleado"),
    path('gestionar_empleados/', views.gestionar_empleados,name="gestionar_empleados"),
    path('editar_empleado/<int:empleado_id>', views.editar_empleado, name="editar_empleado" ),
    path('eliminar_empleado/<int:user_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('filtrar/', views.filtrar_productos_por_filtro, name='filtrar_productos_por_filtro'),
    path('aceptar_trueque/<int:obj_id>/', views.aceptar_trueque, name='aceptar_trueque'),
    path('rechazar_trueque/<int:obj_id>/', views.rechazar_trueque, name='rechazar_trueque'),
    path('cancelar_trueque/<int:trueque_id>/', views.cancelar_trueque, name='cancelar_trueque'),
    path('intercambios_aceptados/<int:intercambio_id>', views.historial_aceptados,name='intercambios_aceptados'),
    path('intercambios_aceptados/', views.historial_aceptados, name='intercambios_aceptados'),
    path('ver_mis_objetos_postulados/',views.mis_objetos_postulados,name="ver_mis_objetos_postulados"),
    path('rate/<int:intercambio_id>/', views.rate_profile, name='rate_profile'),
    path('rate/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('ver_estadisticas/', views.ver_estadisticas,name="ver_estadisticas"),
    path('estadisticas_intercambios/', views.ver_estadisticas_intercambio,name="estadisticas_intercambios")

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)