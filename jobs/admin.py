from django.contrib import admin

# Register your models here.
from .models import Job, Application, Employer

admin.site.register([Job, Application, Employer])