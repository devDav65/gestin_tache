from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display =('titre', 'description','date_creation','completed')
    search_fields =('titre',)
    list_filter =('date_creation','completed')