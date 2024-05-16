from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
#class Estadistica(models.Model):                          #clase por si quisiera agregar estadisticas ahora 
    #title = models.CharField(max_length=200)

class Sucursal(models.Model):
    title= models.CharField(max_length=200)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

class intercambios(models.Model):
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    categoria = models.CharField(max_length=200)
    foto = models.ImageField()
    descripcion = models.CharField(max_length=200, default="")
    modelo = models.CharField(max_length=200, default="")
    marca = models.CharField(max_length=200,default="")
   
    