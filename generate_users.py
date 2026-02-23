# generate_users.py

import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

from enums import (
    DEVICE_TYPES,
    OS_BY_DEVICE,
    GEO_HIERARCHY,
)

# =========================================================
# 1. STABLE RANDOMNESS (must match ads generator)
# =========================================================

SEED = 51
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

# =========================================================
# 2. GLOBAL PARAMETERS
# =========================================================

N_USERS = 10_000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 1, 1)

USER_SEGMENTS = ["ad_supported", "premium", "kids"]
SEGMENT_WEIGHTS = [0.55, 0.35, 0.10]

AGE_BUCKETS = ["13-17", "18-24", "25-34", "35-44", "45-54", "55+"]
AGE_WEIGHTS = [0.08, 0.22, 0.28, 0.20, 0.14, 0.08]

# =========================================================
# 3. HELPERS (shared logic with ads generator)
# =========================================================


def sample_geo():
    country = random.choice(list(GEO_HIERARCHY.keys()))
    region = random.choice(list(GEO_HIERARCHY[country].keys()))
    city = random.choice(GEO_HIERARCHY[country][region])
    return country, region, city


def sample_device_os():
    device = random.choice(DEVICE_TYPES)
    os = random.choice(OS_BY_DEVICE[device])
    return device, os


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


# =========================================================
# 4. USER GENERATION
# =========================================================

users = []

for i in range(N_USERS):
    user_id = f"user_{i}"

    signup_date = random_date(START_DATE, END_DATE)
    first_seen_date = signup_date
    last_seen_date = signup_date + timedelta(days=random.randint(1, 180))

    user_segment = random.choices(USER_SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
    age_bucket = random.choices(AGE_BUCKETS, weights=AGE_WEIGHTS)[0]

    device_type, os = sample_device_os()
    country, region, city = sample_geo()

    users.append(
        {
            "user_id": user_id,
            "signup_date": signup_date.date(),
            "first_seen_date": first_seen_date.date(),
            "last_seen_date": last_seen_date.date(),
            "user_segment": user_segment,
            "age_bucket": age_bucket,
            "primary_device_type": device_type,
            "primary_os": os,
            "country": country,
            "region": region,
            "city": city,
            "is_kids_profile": user_segment == "kids",
            "updated_at": last_seen_date,
        }
    )

    # =========================================================
# 5. WRITE OUTPUT
# =========================================================

df = pd.DataFrame(users)
df.to_csv("users.csv", index=False)

print(f"Generated {len(df):,} users")
