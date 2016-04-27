from django.contrib import admin
from .models import student,faculty,studentTemplateDesign,facultyTemplateDesign
# Register your models here.

admin.site.register(student)
admin.site.register(studentTemplateDesign)
admin.site.register(faculty)
admin.site.register(facultyTemplateDesign)
