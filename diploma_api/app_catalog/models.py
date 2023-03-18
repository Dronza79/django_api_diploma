from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    parent = models.ForeignKey(
        'self', on_delete=models.PROTECT, null=True, blank=True,
        related_name='subcategories', verbose_name='Родительская категория')

    def __str__(self):
        return self.title

    @admin.display(description='Изображение')
    def get_icon(self):
        if self.image:
            return mark_safe(f'<img src={self.image.src.url}>')
        else:
            return 'Нет изображения'

    @property
    @admin.display(description='Относительный путь')
    def href(self):
        return f'/catalog/{self.pk}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Image(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='image')
    src = models.FileField(upload_to='category/', verbose_name='Выбор файла')
    alt = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if not self.alt:
            self.alt = 'картинка ' + str(self.category.title)
        super().save(*args, **kwargs)
