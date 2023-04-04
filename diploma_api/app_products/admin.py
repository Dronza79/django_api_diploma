from django.contrib import admin

from .models import Product, ImageProduct, PropertyProduct, TitleProperty, Review, Tag


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
    verbose_name = 'Отзыв'
    verbose_name_plural = "Отзывы"
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_per_page = 25
    list_filter = ["category"]
    list_display = [
        'id', 'title', 'category', 'price', 'count', 'slug',
        "date", 'rating', 'total_review', 'limited'
    ]
    filter_horizontal = 'tags',
    list_display_links = ['title']
    list_editable = ['price', 'count', 'limited']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        PropertyInline,
        GalleryInline,
        ReviewInLine,
    ]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        ('Теги', {
            'classes': ('collapse',),
            'fields': ('tags',)
        }),
        ('Настройки продаж', {
            'classes': 'wide',
            'fields': (('price', 'count'), 'limited'),
        }),
        ('Категория и описание', {
            'classes': 'wide',
            'fields': ('category', 'description', 'fullDescription',),
        }),)


register_hidden_models(TitleProperty, Review)


class ProductInline(admin.TabularInline):
    model = Product.tags.through
    verbose_name = "Продукты"
    verbose_name_plural = "Продукты"
    extra = 1


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'id': ('name',)}
    inlines = [ProductInline]

