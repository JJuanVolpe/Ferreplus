from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),    
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name="about"),
    path('hello/<str:username>', views.hello, name="hello"),
    path('projects/', views.projects, name="projects"),
    path('projects/<int:id>', views.project_detail, name="project_detail"),
    path('tasks/', views.tasks, name="tasks"),
    path('create_task/', views.create_task, name="create_task"),
    path('create_project/', views.create_project, name="create_project"),
]