# Искажение данных
import numpy as np
import pandas as pd


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
