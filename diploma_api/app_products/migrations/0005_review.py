# Generated by Django 4.1.7 on 2023-03-16 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0004_alter_imageproduct_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=150, verbose_name='Автор отзыва')),
                ('email', models.CharField(blank=True, max_length=250, verbose_name='Почта автора')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('rate', models.PositiveSmallIntegerField(verbose_name='Рейтинг')),
                ('text', models.TextField(verbose_name='Содержание отзыва')),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_products.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы о товарах',
            },
        ),
    ]
