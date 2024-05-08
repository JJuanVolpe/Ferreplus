from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name="about"),
    path('hello/<str:username>', views.hello, name="hello"),
    path('projects/', views.projects, name="projects"),
    path('sucursales/',views.Sucursales,name='Sucursales'),
    path('intercambios/',views.Menu_intercambios,name="Menu_De_Intercambios"),
    path('historial-intercambios/',views.Historial_Intercambios, name="Historial_De_Intercambios"),
    path('mis-trueques/',views.Ver_Trueques, name="Mis_Trueques"),
    path('crear-trueques/',views.Crear_Trueque,name="Crear_Trueques"),
    path('menu-sucursales/',views.Menu_Sucursales, name="Menu_Sucursales"),
    path('eliminar_sucursal/<int:sucursal_id>/', views.eliminar_sucursal, name='eliminar_sucursal'),
    path('editar_sucursal/<int:sucursal_id>/', views.editar_sucursal, name='editar_sucursal')
]