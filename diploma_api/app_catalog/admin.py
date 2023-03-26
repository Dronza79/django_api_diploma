from django.contrib import admin

from .models import Category, Image


class IconInline(admin.TabularInline):
    model = Image
    readonly_fields = ('alt',)
    verbose_name = "Изображение"
    verbose_name_plural = "Изображение"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ['id', 'title', 'parent', 'href', 'get_icon']
    inlines = [IconInline]

