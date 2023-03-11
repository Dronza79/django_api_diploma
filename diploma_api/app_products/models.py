import transliterate
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
    specifications = models.ManyToManyField('TitleProperty', through='PropertyProduct')

    # date = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    # available = models.BooleanField(default=True, verbose_name='В продаже')
    # limited = models.BooleanField(default=False, verbose_name='Ограниченная серия')
    # extra_data = models.ManyToManyField("TitleData", through='ExtraData', verbose_name='Дополнительные данные')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(f'{self.title}')
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['category']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    @property
    def href(self):
        return f'/catalog/{self.pk}'

    @property
    def rating(self):
        return 4.5
        # return sum(item.rate for item in self.reviews.all()) / self.reviews.count()

    @property
    def freeDelivery(self):
        # settings = SiteSettings.load()
        # return self.price > settings.min_cost_for_free_delivery
        return True

    @property
    def tags(self):
        return []

    @property
    def reviews(self):
        return []


def get_upload_path(instance, filename):
    return f'products/{instance.product.slug}/{filename}'


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
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
    device = models.ForeignKey(Product, related_name='properties', on_delete=models.CASCADE, verbose_name='Устройство')
    name = models.ForeignKey(TitleProperty, on_delete=models.CASCADE, verbose_name='Заголовок')
    value = models.CharField(max_length=255, verbose_name='Значение характеристики')

    def __str__(self):
        return f'name={self.name}, value={self.value}'

    class Meta:
        verbose_name = "Характеристики"
        verbose_name_plural = "Характеристики"

    # @property
    # def total_review(self):
    #     return len(self.comments.all())

    # @property
    # @admin.display(description='Наименование')
    # def get_full_name(self):
    #     return f'{self.type_device} {self.fabricator} {self.model}'

    # @property
    # def total_review(self):

    # @property
    # def in_stock(self):
    #     return self.stock != 0
    #
    # @property
    # def total_sale(self):

    #     return sum(item.quantity for item in self.order_items.all())


# class TitleData(models.Model):
#     title = models.CharField(max_length=100, verbose_name='Заголовок')
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = "Наименование"
#         verbose_name_plural = "Наименования"
#
#
# class ValueData(models.Model):
#     value = models.CharField(max_length=100, verbose_name='Заголовок')
#
#     def __str__(self):
#         return self.value
#
#     class Meta:
#         verbose_name = "Значение"
#         verbose_name_plural = "Значения"
#
#
# class ExtraData(models.Model):
#     title = models.ForeignKey(TitleData, related_name='extradata', on_delete=models.CASCADE, verbose_name="Параметр")
#     device = models.ForeignKey(
#         Product, related_name='extradata', on_delete=models.CASCADE, verbose_name='Устройство', db_index=True,)
#     value = models.ForeignKey(ValueData, related_name='extradata', on_delete=models.CASCADE, verbose_name="Значение")
#
#     def __str__(self):
#         return f'{self.title}: {self.value}'
#
#     class Meta:
#         verbose_name = "Дополнительные данные"
#         verbose_name_plural = "Сведения"
