import pandas as pd
import numpy as np

from datetime import date, timedelta
from faker import Faker


fake = Faker()

def generate_users(n=3000):
    channels = ['organic', 'paid_search', 'social', 'referral', 'email']
    channel_probs = [0.45, 0.25, 0.15, 0.10, 0.05]

    plan_probs_by_channel = { 
    'organic': [0.7, 0.2, 0.1], # [free, basic, pro]
    'paid_search': [0.3, 0.4, 0.3], 
    'social': [0.6, 0.3, 0.1],
    'referral': [0.4, 0.35, 0.25],
    'email': [0.5, 0.25, 0.25]
    }

    countries = ["Russia", "Belarus", "China", "Spain"]
    countries_probs = [0.5, 0.3, 0.15, 0.05]

    start = date.today() - timedelta(days=18*30)
    end = date.today()

    users = []

    for i in range(n):
        channel = np.random.choice(channels, p=channel_probs)
        plan = np.random.choice(['free', 'basic', 'pro'], p=plan_probs_by_channel[channel])
        country = np.random.choice(countries, p=countries_probs)
        signup_date = fake.date_between(start_date=start, end_date=end)
        users.append({'acquisition_channel': channel, 'plan': plan, 'country': country, 'signup_date': signup_date})

    return pd.DataFrame(users)
