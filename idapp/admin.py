from django.contrib import admin
from .models import stud,faculty,SDesign,FDesign
# Register your models here.

admin.site.register(stud)
admin.site.register(SDesign)
admin.site.register(faculty)
admin.site.register(FDesign)
