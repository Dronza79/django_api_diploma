from django.urls import path

from .views import *

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('avatar', ProfileAvatarView.as_view(), name='avatar'),
    path('password', ChangePasswordView.as_view(), name='password'),
]
