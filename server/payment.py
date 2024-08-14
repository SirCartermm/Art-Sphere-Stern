import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_payment_intent(amount, currency):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],

        )
        return intent
    except Exception as e:
        return str(e)
    