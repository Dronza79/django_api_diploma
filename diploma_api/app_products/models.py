import re
from statistics import mean

from transliterate import translit, slugify, detect_language
from django.contrib import admin
from django.db import models


class Product(models.Model):
    category = models.ForeignKey('app_catalog.Category', on_delete=models.PROTECT, related_name='products',
                                 verbose_name="Категория товара")
    title = models.CharField(max_length=50, verbose_name='Название', default='')
    description = models.CharField(max_length=200, verbose_name='Короткое описание', default='')
    slug = models.SlugField(max_length=255, null=False, unique=True, verbose_name="URL товара", default='')
    fullDescription = models.TextField(blank=True, verbose_name='Описание', default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    count = models.PositiveIntegerField(verbose_name='В наличии', default=0)
    date = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    limited = models.BooleanField(verbose_name='Лимитированные товары', default=False)
    feature = models.ManyToManyField('TitleProperty', through='PropertyProduct')
    tags = models.ManyToManyField('Tag', verbose_name='Таги', related_name='products')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not re.fullmatch(r'[а-яА-ЯёЁ]+', self.title):
            self.slug = slugify(translit(self.title, 'ru'))
        else:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['category']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    @admin.display(description='Количество отзывов')
    def total_review(self):
        return int(self.reviews.count())

    @property
    def href(self):
        return f'/product/{self.pk}'

    @property
    def images(self):
        return [str(img) for img in self.pictures.all()]

    @property
    @admin.display(description='Рейтинг')
    def rating(self):
        if not self.reviews.all():
            return None
        return round(mean(item.rate for item in self.reviews.all()), 1)

    @property
    def freeDelivery(self):
        # settings = SiteSettings.load()
        # return self.price > settings.min_cost_for_free_delivery
        return True

    # @property
    # def tags(self):
    #     return []

    # @property
    # def count_reviews(self):
    #     return []


def get_upload_path(instance, filename):
    return f'products/{instance.product.slug}/{filename}'


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    pic = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return str(self.pic.url)


class TitleProperty(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Свойство"
        verbose_name_plural = "Свойства"


class PropertyProduct(models.Model):
    device = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE, verbose_name='Устройство')
    name = models.ForeignKey(TitleProperty, on_delete=models.CASCADE, verbose_name='Заголовок')
    value = models.CharField(max_length=255, verbose_name='Значение характеристики')

    def __str__(self):
        return f'name={self.name}, value={self.value}'

    class Meta:
        verbose_name = "Характеристики"
        verbose_name_plural = "Характеристики"


class Review(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='reviews')
    author = models.CharField(max_length=150, verbose_name='Автор отзыва')
    email = models.CharField(max_length=250, verbose_name='Почта автора', blank=True)
    date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    rate = models.PositiveSmallIntegerField(verbose_name='Рейтинг')
    text = models.TextField(verbose_name='Содержание отзыва')

    def __str__(self):
        return f'отзыв {self.author} о {self.prod.title}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы о товарах"


class Tag(models.Model):
    name = models.CharField(max_length=20)
    id = models.SlugField(max_length=20, blank=True, primary_key=True)

    def save(self, *args, **kwargs):
        if not re.fullmatch(r'[а-яА-ЯёЁ]+', self.name):
            self.id = slugify(translit(self.name, 'ru'))
        else:
            self.id = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
