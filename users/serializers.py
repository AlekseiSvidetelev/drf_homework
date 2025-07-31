from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PublicUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "tg_name", "avatar")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
