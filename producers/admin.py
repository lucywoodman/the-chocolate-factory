from django.contrib import admin
from .models import Producer


class ProducerAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    ordering = ("location",)


admin.site.register(Producer, ProducerAdmin)
