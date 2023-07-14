from django.contrib import admin

# Register your models here.
from .models import Municipal,Employee,Qada,Province


admin.site.register(Municipal)
admin.site.register(Employee)
admin.site.register(Qada)
admin.site.register(Province)