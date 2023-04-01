from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_upload_path_avatar(instance, filename):
    return f'avatar/{instance.user.username}/{filename}'


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    print('kwargs=', kwargs)
    print('user=', instance)
    if created:
        Profile.objects.create(user=instance)


class Profile(models.Model):
    fullName = models.CharField(max_length=255, verbose_name='Полное имя', blank=True)
    email = models.EmailField(verbose_name='Почта', blank=True)
    phone = models.CharField(max_length=15, verbose_name='Телефон', blank=True)
    avatar = models.FileField(upload_to=get_upload_path_avatar, verbose_name='Аватар', blank=True)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'Профиль {self.user}'
