from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from uploadApp.models import Patient, PatientReport, User, Hospital

# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(PatientReport)
admin.site.register(Hospital)