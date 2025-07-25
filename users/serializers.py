from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "tg_name", "avatar")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
