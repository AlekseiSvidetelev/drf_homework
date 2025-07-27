from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone", "tg_name", "avatar")


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "phone", "tg_name")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
