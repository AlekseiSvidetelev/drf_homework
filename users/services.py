import os

import stripe
from forex_python.converter import CurrencyRates
from stripe import Price, Product

from users.models import Payment

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def convert_rub_to_usd(amount: int) -> int:
    """Конвертация рублей в доллары"""
    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(float(amount) * rate)


def create_stripe_product(payment: Payment) -> Product:
    """Создает продукт в Stripe"""
    if payment.paid_course:
        name = f"Курс: {payment.paid_course.title}"
    else:
        name = f"Урок: {payment.paid_lesson.title}"
    description = name[:500]
    return stripe.Product.create(name=name[:255], description=description)


def create_stripe_product_price(amount: int, product_id: str) -> stripe.Price:
    """Создает цену на товар"""
    stripe_price = stripe.Price.create(
        currency="usd",
        unit_amount=convert_rub_to_usd(amount),
        product=product_id,
    )
    return stripe_price


def create_stripe_session(price: Price) -> tuple:
    """Создает сессию для оплаты"""

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
        metadata={"payment_id": price.id},
    )
    return session.id, session.url
