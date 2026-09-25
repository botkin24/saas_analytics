# Искажение данных
import numpy as np
import pandas as pd

# ----- USERS -----


# В 5% строках сделаем поле "country" как Nan | Таблица "users"
def make_country_nan(df):
    df_users = df.copy()

    random_rows = df_users.sample(frac=0.05).index
    df_users.loc[random_rows, "country"] = np.nan

    return df_users


# Для всех юзеров из Испании сделаем поле "signup_date" как Nan | Таблица "users"
def make_spain_signup(df):
    df_users = df.copy()

    df_users.loc[df_users["country"] == "Spain", "signup_date"] = np.nan

    return df_users


# Делаем написание "Russia" разными вариантами | Таблица "users"
def add_country_case_variants(df):
    df_users = df.copy()

    variants = ["russia", "Rusia", "RU"]
    russia_rows = df_users[df_users["country"] == "Russia"]
    sample_rows = russia_rows.sample(frac=0.3).index

    df_users.loc[sample_rows, "country"] = np.random.choice(
        variants, size=len(sample_rows)
    )

    return df_users


# Добавим дубликаты | Таблица "users"
def add_duplicate_rows(df):
    df_users = df.copy()

    duplicate_rows = df_users.sample(frac=0.03)
    df_users = pd.concat([df_users, duplicate_rows])

    return df_users


# Приведем "signup_date" к строковому типу | Таблица "users"
def add_signup_date_string_format(df, frac=0.3, random_state=42):
    df_users = df.copy()

    # Приводим столбец к datetime
    original_dates = pd.to_datetime(df_users["signup_date"])
    df_users["signup_date"] = original_dates

    # Выбираем случайные 30% индексов
    str_rows = df_users.sample(frac=frac, random_state=random_state).index

    # Список форматов
    formats = [
        "%Y-%m-%d",  # 2026-09-22
        "%d/%m/%Y",  # 22/09/2026
        "%m-%d-%Y",  # 09-22-2026
    ]

    # Делим массив на 3 части (количество форматов)
    groups = np.array_split(str_rows, len(formats))

    # Явно преобразуем столбец в object
    df_users["signup_date"] = df_users["signup_date"].astype(object)

    # Применяем формат к каждой группе
    for group_idx, fmt in zip(groups, formats):
        if len(group_idx) > 0:
            # Берем даты из original_dates, где гарантированно доступен акцессор .dt
            formatted_dates = original_dates.loc[group_idx].dt.strftime(fmt)
            df_users.loc[group_idx, "signup_date"] = formatted_dates

    return df_users


# Объединений функций | Таблица "users"
def make_users_dirty(df):
    df_users = (
        df.pipe(make_country_nan)
        .pipe(make_spain_signup)
        .pipe(add_country_case_variants)
        .pipe(add_duplicate_rows)
        .pipe(add_signup_date_string_format)
    )

    return df_users


# ----- PAYMENTS -----


# Добавление такого "subscription_id", которого нет в таблице "subscriptions" | Таблица "payments"
def add_subscription_id_anomaly(df):
    df_payments = df.copy()

    random_rows = df_payments.sample(frac=0.01).index
    df_payments.loc[random_rows, "subscription_id"] = np.random.randint(
        9000, 10000, size=len(random_rows)
    )

    return df_payments


# Добавление пропусков в "amount" | Таблица "payments"
def add_amount_gaps(df):
    df_payments = df.copy()

    random_rows = df_payments.sample(frac=0.07).index
    df_payments.loc[random_rows, "amount"] = np.nan

    return df_payments


# Добавление мусорных строк в "amount" | Таблица "payments"
def add_amount_trash_strings(df):
    df_payments = df.copy()
    df_payments["amount"] = df_payments["amount"].astype(object)

    def messify_amount(value):
        fmt = np.random.choice(["space", "dollar", "comma"])
        if fmt == "space":
            return f"{value:,.0f}".replace(",", " ")
        elif fmt == "dollar":
            return f"${value:.2f}"
        else:
            return f"{value:.2f}".replace(".", ",")

    random_rows = df_payments.sample(frac=0.05).index
    df_payments.loc[random_rows, "amount"] = df_payments.loc[
        random_rows, "amount"
    ].apply(messify_amount)

    return df_payments


# Добавление аномальных сумм в "amount" | Таблица "payments"
def add_amount_anomaly(df):
    df_payments = df.copy()

    anomaly_rows = df_payments.index[:5]
    df_payments.loc[anomaly_rows[:2], "amount"] = -50.0
    df_payments.loc[anomaly_rows[2:4], "amount"] = 5000.0
    df_payments.loc[anomaly_rows[4], "amount"] = -999.99

    return df_payments


def make_payments_dirty(df):
    df_payments = (
        df.pipe(add_subscription_id_anomaly)
        .pipe(add_amount_gaps)
        .pipe(add_amount_trash_strings)
        .pipe(add_amount_anomaly)
    )
    return df_payments
