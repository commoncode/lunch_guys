from django.contrib import admin
from lunches import models

# Register your models here.
admin.site.register(models.Menu)
admin.site.register(models.Order)
admin.site.register(models.Item)