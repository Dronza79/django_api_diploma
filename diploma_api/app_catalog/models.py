from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    icon = models.FileField(upload_to='category/', blank=True, verbose_name='Иконка')
    parent = TreeForeignKey(
        'self', on_delete=models.PROTECT, null=True,
        blank=True, related_name='subcategories', verbose_name='Родительская категория')

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @property
    def image(self):
        return {"src": f'http://127.0.0.1:8000{self.icon.url}', 'alt': f'картинка {self.title}'}

    @property
    def href(self):
        return f'catalog/{self.pk}'
