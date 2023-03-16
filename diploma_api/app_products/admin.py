from django.contrib import admin

from .models import Product, ImageProduct, PropertyProduct, TitleProperty, Review


def register_hidden_models(*model_names):
    for model in model_names:
        model_admin = type(
            str(model)+'Admin', (admin.ModelAdmin,), {'get_model_perms': lambda self, request: {}})
        admin.site.register(model, model_admin)


class GalleryInline(admin.TabularInline):
    model = ImageProduct
    verbose_name = "Отображение"
    verbose_name_plural = "Отображения"
    extra = 0


class PropertyInline(admin.TabularInline):
    model = PropertyProduct
    verbose_name = 'Характеристики'
    verbose_name_plural = "Характеристики"
    extra = 0


class ReviewInLine(admin.StackedInline):
    model = Review
    verbose_name = 'Отзывы'
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_per_page = 10
    list_filter = ["category"]
    list_display = [
        'id', 'title', 'category', 'price', 'count', 'slug',
        "date", 'rating', 'total_review'
    ]
    list_display_links = ['title']
    list_editable = ['price', 'count']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        PropertyInline,
        GalleryInline,
        ReviewInLine,
    ]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug',)
        }),
        ('Настройки продаж', {
            'classes': 'wide',
            'fields': (('price', 'count'),),
        }),
        ('Категория и описание', {
            'classes': 'wide',
            'fields': ('category', 'description', 'fullDescription',),
        }),)


register_hidden_models(TitleProperty, Review)
