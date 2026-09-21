# Искажение данных
import numpy as np
import pandas as pd


def make_users_dirty(users_db):
    df_users = users_db.copy()

    random_rows = df_users.sample(frac=0.05).index
    df_users.loc[random_rows, "country"] = np.nan

    return df_users
