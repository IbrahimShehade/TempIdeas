from django.contrib import admin

# Register your models here.
from .models import Province,Qada,Municipal,CustomUser

admin.site.register(Province)
admin.site.register(Qada)
admin.site.register(Municipal)
