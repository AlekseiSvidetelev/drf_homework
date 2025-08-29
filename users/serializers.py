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


class PaymentStripeCreateSerializer(serializers.ModelSerializer):

    payment_url = serializers.SerializerMethodField()

    def get_payment_url(self, obj):
        if obj.stripe.stripe_session_url:
            return obj.stripe.stripe_session_url
        return None

    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "method",
            "payment_url",
        )

    def validate(self, obj):

        if not obj.get("paid_course") and not obj.get("paid_lesson"):
            raise serializers.ValidationError("Необходимо указать курс или урок")
        return obj
