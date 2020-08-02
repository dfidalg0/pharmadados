from django.contrib import admin

from .models import Medicine, Info

# Register your models here.
admin.site.register([Medicine, Info])
