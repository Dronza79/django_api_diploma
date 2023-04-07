from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from app_products.models import Product


class UserCart(models.Model):
    session = models.CharField(verbose_name='Сессия', default='', max_length=40)
    owner = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 related_name='cart',
                                 verbose_name='Чья корзина',
                                 blank=True,
                                 null=True
                                 )
    cart = models.ManyToManyField(Product,
                                  through='InsideCart',
                                  verbose_name='Содержание корзины',
                                  related_name="carts",
                                  blank=True
                                  )

    class Meta:
        verbose_name = "Корзина пользователя"
        verbose_name_plural = "Корзины пользователей"

    def __str__(self):
        return 'Корзина ' + str(self.owner.username) if self.owner else 'Корзина Anonymous'

    def __len__(self):
        return sum(item.quantity for item in self.inside.only('quantity').all())

    def __iter__(self):
        for item in self.inside.all():
            data = {
                'total_price': item.cost * item.quantity,
                'product': item.product,
                'quantity': item.quantity,
                'price': item.cost,
            }
            yield data

    def add(self, product, quantity=1, update_quantity=False):
        cart = self.inside.get_or_create(user_cart=self, product=product)[0]
        if update_quantity:
            cart.quantity = quantity
        else:
            cart.quantity += quantity
        cart.cost = str(product.price)
        cart.save()

    def add_cart(self, cart):
        if cart:
            for goods in cart.inside.all():
                self.add(goods.product, goods.quantity)
            cart.clear()

    def remove(self, product):
        self.cart.remove(product)

    def clear(self):
        self.delete()

    @property
    def get_total_price(self):
        return sum(
            Decimal(item.cost) * item.quantity for item in self.inside.only('quantity', 'cost').all())


class InsideCart(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='inside')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товары', related_name='entry')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость', null=True)

    class Meta:
        verbose_name = "Содержание корзины"
        verbose_name_plural = "Содержание корзин"

    def __str__(self):
        return f'{self.product}={self.quantity} шт.'

    def save(self, *args, **kwargs):
        self.cost = str(self.product.price)
        return super().save(*args, **kwargs)
