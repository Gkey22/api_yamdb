from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import SerializerUser, SerializerUserRegistration


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = SerializerUser
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]


class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = SerializerUserRegistration
    queryset = User.objects.all()
    #permission_classes = [permissions.AllowAny,]
    #lookup_field = settings.USER_ID_FIELD


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = SerializerUser
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return get_object_or_404(User, username=self.request.user)
