from django.contrib import admin
from .models import Profile, Sucursal, intercambios, Product

# Register your models here.
admin.site.register(Profile)
admin.site.register(Sucursal)
admin.site.register(intercambios)
admin.site.register(Product)