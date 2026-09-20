import random
from datetime import date, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()


# Генерация данных для таблицы "users"
def generate_users(n=3000):
    channels = ["organic", "paid_search", "social", "referral", "email"]
    channel_probs = [0.45, 0.25, 0.15, 0.10, 0.05]

    plan_probs_by_channel = {
        "organic": [0.7, 0.2, 0.1],  # [free, basic, pro]
        "paid_search": [0.3, 0.4, 0.3],
        "social": [0.6, 0.3, 0.1],
        "referral": [0.4, 0.35, 0.25],
        "email": [0.5, 0.25, 0.25],
    }

    countries = ["Russia", "Belarus", "China", "Spain"]
    countries_probs = [0.5, 0.3, 0.15, 0.05]

    start = date.today() - timedelta(days=18 * 30)
    end = date.today()

    users = []

    for i in range(n):
        channel = np.random.choice(channels, p=channel_probs)
        plan = np.random.choice(
            ["free", "basic", "pro"], p=plan_probs_by_channel[channel]
        )
        country = np.random.choice(countries, p=countries_probs)
        signup_date = fake.date_between(start_date=start, end_date=end)
        users.append(
            {
                "acquisition_channel": channel,
                "plan": plan,
                "country": country,
                "signup_date": signup_date,
            }
        )

    return pd.DataFrame(users)


# Генерация данных для таблицы "subscription"
def generate_subscription(users_db):
    price_by_plan = {"basic": 100.0, "pro": 250.0}

    paying_user = users_db[users_db["plan"] != "free"]  # только платящие

    subscription = []

    for _, user in paying_user.iterrows():
        user_id = user["id"]
        plan = user["plan"]
        signup_date = user["signup_date"]

        # Дата начала подписки: дата регистрации + случайное количество дней (0-14)
        days_to_subscribe = random.randint(0, 14)
        start_date = signup_date + timedelta(days=days_to_subscribe)

        # Активна подписка или уже отменена (70%/30%)
        status = np.random.choice(["active", "canceled"], p=[0.7, 0.3])

        if status == "active":
            end_date = None
        else:
            # Если отменена, конец где-то после начала (30-300 дн)
            days_active = random.randint(30, 300)
            end_date = start_date + timedelta(days=days_active)

        subscription.append(
            {
                "user_id": user_id,
                "plan": plan,
                "price": price_by_plan[plan],
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
            }
        )

    return pd.DataFrame(subscription)


# Генерация данных для таблицы "payments"
def generate_payments(subscriptions_db):
    payments = []
    today = pd.Timestamp.today().normalize()

    for _, sub in subscriptions_db.iterrows():
        sub_id = sub["id"]
        start_date = sub["start_date"]
        price = sub["price"]

        end_limit = sub["end_date"] if sub["status"] == "canceled" else today

        current_date = start_date
        while current_date <= end_limit:
            # Имитация, что 5% платежей не проходит успешно
            status = np.random.choice(["succeeded", "failed"], p=[0.95, 0.05])
            payments.append(
                {
                    "subscription_id": sub_id,
                    "amount": price,
                    "payment_date": current_date,
                    "status": status,
                }
            )
            current_date += timedelta(days=30)

    return pd.DataFrame(payments)


# Генерация данных для таблицы "ab_test_assignments"
def generate_ab_assignments(users_db):
    tests = ["onboarding", "pricing"]
    variants = ["A", "B"]

    # В тестах участвует пользователи, зарегистрировашиеся не более полугода назад
    six_months_ago = pd.Timestamp.today() - pd.DateOffset(month=6)
    recent_users = users_db[users_db["signup_date"] >= six_months_ago]

    assignments = []

    for _, user in recent_users.iterrows():
        user_id = user["id"]
        signup_date = user["signup_date"]

        for test in tests:
            variant = np.random.choice(variants, p=[0.5, 0.5])
            assigned_at = signup_date + timedelta(days=random.randint(0, 3))

            assignments.append(
                {
                    "user_id": user_id,
                    "test": test,
                    "variant": variant,
                    "assigned_at": assigned_at,
                }
            )

    return pd.DataFrame(assignments)
