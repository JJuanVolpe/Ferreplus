from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Sucursal(models.Model):
    address = models.CharField(max_length=100,default="")
    city = models.CharField(max_length=40, null=True,default="")
    def delete(self, *args, **kwargs):
        profiles = Profile.objects.filter(sucursal=self)
        for profile in profiles:
            if profile.user:
                profile.user.delete()
            profile.delete()
        super().delete(*args, **kwargs)

class Profile(models.Model):
    # otros campos
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", blank=True, null=True)
    edad = models.PositiveBigIntegerField(null=True, blank=False)
    dni = models.CharField(null=True, blank=False, max_length=10)
    genero = models.CharField(null=True, blank=True, max_length=10)
    telefono = models.CharField(null=True, blank=True, max_length=15)
    es_gerente = models.BooleanField(null=False, blank=False,default=False)
    es_empleado = models.BooleanField(null=False, blank=False,default=False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE,related_name="sucursal",null=True,blank=True) 
    def __str__(self):
        return "username of prof:" + self.user.username  + " edad:" + str(self.edad) + ", con dni:" + str(self.dni)  + ", genero: "+ str(self.genero)  + "  y celular:" + str(self.telefono)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)




class intercambios(models.Model):
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    categoria = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='static/fotos_intercambios/')
    descripcion = models.CharField(max_length=200, default="")
    modelo = models.CharField(max_length=200, default="")
    marca = models.CharField(max_length=200,default="")
    usuario = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='intercambios')
    status = models.CharField(max_length=200, null=True, default="NUEVO", blank=True)   # Campo que identitifica estado del trueque
    sucursal_asignada =  models.ForeignKey(Sucursal, on_delete=models.SET_NULL, related_name='intercambios', null=True, blank=True)

    def __str__(self):
        return "intercambio:" + str(self.nombre) + ", con categoria:" + str(self.categoria)  + ", del usuario: "+ str(self.usuario.dni)  + "  y status:" + str(self.status) 



class Product(models.Model):
    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    categoria = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='static/fotos_intercambios/')
    descripcion = models.CharField(max_length=200, default="")
    postulante = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='postulante', null=True, blank=True)
    trueque_postulado = models.ForeignKey(intercambios, on_delete=models.CASCADE, null=True, blank=True)
    hora = models.TimeField(blank=True, null=True)  # Permite valores en blanco y nulos
    fecha = models.DateField(blank=True, null=True)
