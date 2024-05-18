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
    path('intercambio_con_espera_de_ofertas/',views.intercambio_con_espera_de_ofertas,name="intercambio_con_espera_de_ofertas"),
    path('intercambios/',views.Menu_intercambios,name="Menu_De_Intercambios"),
    path('historial-intercambios/',views.Historial_Intercambios, name="Historial_De_Intercambios"),
    path('mis-trueques/',views.Ver_trueques, name="Mis_Trueques"),
    path('crear-trueques/',views.Crear_Trueque,name="Crear_Trueques"),
    path('menu-sucursales/',views.Menu_Sucursales, name="Menu_Sucursales"),
    path('eliminar_sucursal/<int:sucursal_id>/', views.eliminar_sucursal, name='eliminar_sucursal'),
    path('editar_sucursal/<int:sucursal_id>/', views.editar_sucursal, name='editar_sucursal'),
    path('agregar_sucursal/', views.agregar_sucursal, name='agregar_sucursal'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)