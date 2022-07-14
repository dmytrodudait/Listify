from django.contrib import admin
from .models import Listify

class ListifyAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Listify, ListifyAdmin)
