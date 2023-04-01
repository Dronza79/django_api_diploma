# Generated by Django 4.1.7 on 2023-03-31 21:38

import app_profiles.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(blank=True, max_length=255, verbose_name='Полное имя')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Почта')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='Телефон')),
                ('avatar', models.FileField(blank=True, upload_to=app_profiles.models.get_upload_path_avatar, verbose_name='Аватар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]