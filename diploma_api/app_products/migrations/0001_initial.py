# Generated by Django 4.1.7 on 2023-03-11 07:59

import app_products.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50, verbose_name='Тип устройства')),
                ('description', models.CharField(default='', max_length=200, verbose_name='Короткое описание')),
                ('slug', models.SlugField(default='', max_length=255, unique=True, verbose_name='URL товара')),
                ('fullDescription', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='В наличии')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='app_catalog.category', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['category'],
            },
        ),
        migrations.CreateModel(
            name='TitleProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Свойство',
                'verbose_name_plural': 'Свойства',
            },
        ),
        migrations.CreateModel(
            name='PropertyProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Значение характеристики')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='app_products.product', verbose_name='Устройство')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_products.titleproperty', verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Характеристики',
                'verbose_name_plural': 'Характеристики',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.ManyToManyField(through='app_products.PropertyProduct', to='app_products.titleproperty'),
        ),
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.FileField(upload_to=app_products.models.get_upload_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_products.product')),
            ],
        ),
    ]