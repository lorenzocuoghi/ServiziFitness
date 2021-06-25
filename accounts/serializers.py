from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Profile


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
