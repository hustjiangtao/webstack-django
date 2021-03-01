from django.contrib import admin

from .models import Website
from .models import Category
from .models import StaticFile

# Register your models here.

models = (
    Website,
    Category,
    StaticFile,
)
admin.site.register(models)
