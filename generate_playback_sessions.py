# generate_playback_sessions.py

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
# STABLE RANDOMNESS
# =========================================================

SEED = 51
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

# =========================================================
# PARAMETERS
# =========================================================

N_USERS = 10000
START_DATE = datetime(2026, 1, 1)
DAYS = 30

AVG_SESSIONS_PER_DAY = 0.9
AVG_SESSION_DURATION_MIN = 42

CONTENT_TYPES = ["movie", "episode"]
CONTENT_TYPE_WEIGHTS = [0.45, 0.55]

# =========================================================
# HELPERS
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


# =========================================================
# GENERATE PLAYBACK SESSIONS
# =========================================================

sessions = []

for i in range(N_USERS):
    user_id = f"user_{i}"
    device_type, os = sample_device_os()
    country, region, city = sample_geo()

    for day in range(DAYS):
        session_count = max(0, int(random.gauss(AVG_SESSIONS_PER_DAY, 0.6)))

        for _ in range(session_count):
            session_id = fake.uuid4()
            start_ts = START_DATE + timedelta(days=day, minutes=random.randint(0, 1440))

            duration_min = max(5, int(random.gauss(AVG_SESSION_DURATION_MIN, 15)))
            end_ts = start_ts + timedelta(minutes=duration_min)

            content_type = random.choices(CONTENT_TYPES, CONTENT_TYPE_WEIGHTS)[0]

            sessions.append(
                {
                    "playback_session_id": session_id,
                    "user_id": user_id,
                    "content_id": f"{content_type}_{random.randint(1, 500)}",
                    "content_type": content_type,
                    "session_start_ts": start_ts,
                    "session_end_ts": end_ts,
                    "session_duration_minutes": duration_min,
                    "device_type": device_type,
                    "os": os,
                    "country": country,
                    "region": region,
                    "city": city,
                    "is_binge": duration_min > 60,
                    "created_at": start_ts,
                }
            )

# =========================================================
# WRITE OUTPUT
# =========================================================

df = pd.DataFrame(sessions)
df.to_csv("playback_sessions.csv", index=False)

print(f"Generated {len(df):,} playback sessions")
