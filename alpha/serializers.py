from rest_framework import serializers
from .models import ExchangeRate
from django.contrib.auth import get_user_model


class ExchangeRateSerializer(serializers.ModelSerializer):
    """serializes data from the model 

    Args:
        serializers (django db model): it gets the django db model named ExchangeRate
    """

    class Meta:
        model = ExchangeRate
        fields = '__all__'


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
