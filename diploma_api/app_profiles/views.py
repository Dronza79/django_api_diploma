from rest_framework import generics

from .models import Profile
from .serializers import ProfileSerializer, ProfileAvatarSerializer, PasswordSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        print('user=', self.request.user)
        return Profile.objects.get(user=self.request.user)


class ProfileAvatarView(ProfileView):
    serializer_class = ProfileAvatarSerializer

    def post(self, request, *args, **kwargs):
        print('request.data=', request.data)
        return self.update(request, *args, **kwargs)


class ChangePasswordView(generics.RetrieveUpdateAPIView):
    serializer_class = PasswordSerializer

    def get_object(self):
        print('user=', self.request.user)
        return self.request.user
