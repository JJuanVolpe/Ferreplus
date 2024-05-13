from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)




    def __str__(self):
        return self.title + ' - ' + self.project.name
    
    
class Profile(models.Model):
    # otros campos
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", blank=True, null=True)
    edad = models.PositiveBigIntegerField(null=True, blank=False)
    dni = models.CharField(null=True, blank=False, max_length=10)
    genero = models.CharField(null=True, blank=True, max_length=10)
    telefono = models.CharField(null=True, blank=True, max_length=15)
    

    def __str__(self):
        return "edad:" + str(self.edad) + ", con dni:" + str(self.dni)  + ", genero: "+ str(self.genero)  + "  y celular:" + str(self.telefono)  + " - & - "



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)



class Sucursal(models.Model):
    title= models.CharField(max_length=200)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)

    
