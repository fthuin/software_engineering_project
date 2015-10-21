from django.contrib import admin
from tennis.models import Extra,Participant,Court
# Register your models here.
admin.site.register(Participant)
admin.site.register(Extra)
admin.site.register(Court)
