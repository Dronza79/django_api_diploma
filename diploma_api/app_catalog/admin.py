from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from app_catalog.models import Category


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['title']


admin.site.register(Category, CategoryAdmin)
