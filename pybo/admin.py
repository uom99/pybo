from django.contrib import admin
from .models import question


class questionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(question, questionAdmin)
