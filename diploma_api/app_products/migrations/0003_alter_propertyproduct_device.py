# Generated by Django 4.1.7 on 2023-03-11 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0002_rename_specifications_product_feature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyproduct',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='app_products.product', verbose_name='Устройство'),
        ),
    ]
