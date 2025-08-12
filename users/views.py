from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.paginators import CustomPageNumberPagination
from users.models import Payment, PaymentStripe, Subscription, User
from users.permissions import IsOwnerOrAdmin
from users.serializers import PaymentSerializer, PaymentStripeCreateSerializer, PublicUserSerializer, UserSerializer
from users.services import (
    convert_rub_to_usd,
    create_stripe_product,
    create_stripe_product_price,
    create_stripe_session,
)


@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description=(
            "Удаление пользователя по идентификатору. "
            "Требует прав администратора или пользователя.\n\n"
            "**Параметры пути:**\n"
            "- `id` (int): Идентификатор пользователя\n\n"
            "**Ответы:**\n"
            "- `HTTP 204 No Content`: Успешное удаление\n"
            "- `HTTP 404 Not Found`: Пользователь не найден\n"
            "- `HTTP 403 Forbidden`: Нет прав для удаления\n\n"
        ),
        responses={204: "Пользователь успешно удалён", 403: "Доступ запрещён", 404: "Пользователь не найден"},
    ),
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    ordering = ["id"]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            requested_user_id = self.kwargs.get("pk")
            current_user_id = self.request.user.id
            if str(current_user_id) == str(requested_user_id):
                return UserSerializer
        elif self.action == "create":
            return UserSerializer
        return PublicUserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [
                IsAuthenticated,
            ]
        elif self.action == "create":
            self.permission_classes = [
                AllowAny,
            ]
        elif self.action == "retrieve":
            self.permission_classes = [
                IsAuthenticated,
            ]
        elif self.action == "update" or self.action == "partial_update":
            self.permission_classes = [
                IsOwnerOrAdmin,
            ]
        elif self.action == "destroy":
            self.permission_classes = [
                IsOwnerOrAdmin,
            ]
        return super().get_permissions()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["payments"],
        operation_summary="payments_list",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["payments"],
        operation_summary="payments_create",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["payments"],
        operation_summary="payments_read",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["payments"],
        operation_summary="payments_delete",
        operation_description=(
            "Удаление платежа по идентификатору. "
            "Требует прав администратора или владельца платежа.\n\n"
            "**Параметры пути:**\n"
            "- `id` (int): Идентификатор платежа\n\n"
            "**Ответы:**\n"
            "- `HTTP 204 No Content`: Успешное удаление\n"
            "- `HTTP 404 Not Found`: Платёж не найден\n"
            "- `HTTP 403 Forbidden`: Нет прав для удаления\n\n"
            "**Важно:** Удаление платежа невозможно после его обработки системой."
        ),
        responses={204: "Платёж успешно удалён", 403: "Доступ запрещён", 404: "Платёж не найден"},
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["payments"],
        operation_summary="payments_update",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["payments"],
        operation_summary="payments_partial_update",
    ),
)
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    ordering = ["-payment_date"]
    # сортировка и фильтрация
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ("payment_date", "-payment_date")
    filterset_fields = (
        "method",
        "paid_course",
        "paid_lesson",
    )

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Добавление или удаление подписки на курс.",
        operation_summary="user_course_subscription",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "course": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID курса"),
            },
            required=["course"],
        ),
        responses={
            200: openapi.Response(description="подписка удалена"),
            201: openapi.Response(description="подписка добавлена"),
        },
    ),
)
class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})



class PaymentStripeCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentStripeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(payment)
        price = create_stripe_product_price(payment.amount, product.id)
        session_id, payment_link = create_stripe_session(price)

        PaymentStripe.objects.create(
            payment=payment,
            stripe_session_id=session_id,
            stripe_session_url=payment_link,
        )

        payment.session_id = session_id
        payment.session_url = payment_link
        payment.save()
