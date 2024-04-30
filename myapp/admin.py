from django.contrib import admin
from .models import Project, Task, Profile

# Register your models here.
admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(Project)