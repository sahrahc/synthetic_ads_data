###########################################################
# # Generate synthetic ad events data
# Analytics validation
# Ads modeling
# Retention studies
# ML feature testing
###########################################################

import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

from enums import (
    DEVICE_TYPES,
    OS_BY_DEVICE,
    PLACEMENTS,
    GEO_HIERARCHY,
)

# =========================================================
# 1. STABLE RANDOMNESS (deterministic runs)
# for regression testing and reproducible dashboards,
#    same retention curves and same funnel counts
# =========================================================

SEED = 51
random.seed(SEED)

fake = Faker()
Faker.seed(SEED)

# =========================================================
# 3. GLOBAL PARAMETERS
# =========================================================

N_USERS = 10000
DAYS = 30
START_DATE = datetime(2026, 1, 1)

BASE_IMPRESSION_TO_CLICK = 0.09
BASE_CLICK_TO_CONVERSION = 0.01

AVG_SESSIONS_PER_DAY = 1.3
AVG_EVENTS_PER_SESSION = 4

# =========================================================
# 4. HELPER FUNCTIONS
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


def sample_placement():
    return random.choice(PLACEMENTS)


def retention_days():
    """
    Explicit exponential retention decay.
    Higher weight on early days, long tail on later days.
    """
    weights = [0.6**d for d in range(DAYS)]
    return random.choices(range(1, DAYS + 1), weights=weights)[0]


def view_duration_ms(event_type, placement):
    base = {
        "impression": (3_000, 10_000),
        "click": (2_000, 8_000),
        "conversion": (5_000, 20_000),
    }[event_type]

    return int(random.randint(*base) * placement["view_boost"])


# =========================================================
# 5. DATA GENERATION
# =========================================================

users = [f"user_{i}" for i in range(N_USERS)]
events = []

for user_id in users:
    # how many days the users stays active. Most users churn quickly;
    # long-tail power users for a realistic retention curve
    active_days = retention_days()
    device_type, os = sample_device_os()
    country, region, city = sample_geo()

    for day in range(active_days):
        session_count = max(1, int(random.gauss(AVG_SESSIONS_PER_DAY, 0.5)))

        for _ in range(session_count):
            session_id = fake.uuid4()
            session_start = START_DATE + timedelta(
                days=day, minutes=random.randint(0, 1440)
            )

            placement = sample_placement()
            events_in_session = max(1, int(random.gauss(AVG_EVENTS_PER_SESSION, 1)))

            for _ in range(events_in_session):
                event_ts = session_start + timedelta(seconds=random.randint(0, 600))

                # ----------------------------
                # Impression
                # ----------------------------
                events.append(
                    {
                        "event_id": fake.uuid4(),
                        "session_id": session_id,
                        "user_id": user_id,
                        "ad_id": f"ad_{random.randint(1, 200)}",
                        "campaign_id": f"camp_{random.randint(1, 20)}",
                        "event_type": "impression",
                        "event_timestamp": event_ts,
                        "device_type": device_type,
                        "os": os,
                        "country": country,
                        "region": region,
                        "city": city,
                        "surface": placement["surface"],
                        "placement": placement["placement"],
                        "position": placement["position"],
                        "revenue_usd": 0.0,
                        "cost_usd": round(random.uniform(0.001, 0.02), 4),
                        "view_duration_ms": view_duration_ms("impression", placement),
                        "is_billable": True,
                    }
                )

                # ----------------------------
                # Click
                # ----------------------------
                if (
                    random.random()
                    < BASE_IMPRESSION_TO_CLICK * placement["click_boost"]
                ):
                    events.append(
                        {
                            "event_id": fake.uuid4(),
                            "session_id": session_id,
                            "user_id": user_id,
                            "ad_id": f"ad_{random.randint(1, 200)}",
                            "campaign_id": f"camp_{random.randint(1, 20)}",
                            "event_type": "click",
                            "event_timestamp": event_ts,
                            "device_type": device_type,
                            "os": os,
                            "country": country,
                            "region": region,
                            "city": city,
                            "surface": placement["surface"],
                            "placement": placement["placement"],
                            "position": placement["position"],
                            "revenue_usd": 0.0,
                            "cost_usd": round(random.uniform(0.05, 0.50), 2),
                            "view_duration_ms": view_duration_ms("click", placement),
                            "is_billable": True,
                        }
                    )

                    # ----------------------------
                    # Conversion
                    # ----------------------------
                    if random.random() < BASE_CLICK_TO_CONVERSION:
                        revenue = round(random.uniform(5, 150), 2)
                        events.append(
                            {
                                "event_id": fake.uuid4(),
                                "session_id": session_id,
                                "user_id": user_id,
                                "ad_id": f"ad_{random.randint(1, 200)}",
                                "campaign_id": f"camp_{random.randint(1, 20)}",
                                "event_type": "conversion",
                                "event_timestamp": event_ts,
                                "device_type": device_type,
                                "os": os,
                                "country": country,
                                "region": region,
                                "city": city,
                                "surface": placement["surface"],
                                "placement": placement["placement"],
                                "position": placement["position"],
                                "revenue_usd": revenue,
                                "cost_usd": round(
                                    revenue * random.uniform(0.2, 0.6), 2
                                ),
                                "view_duration_ms": view_duration_ms(
                                    "conversion", placement
                                ),
                                "is_billable": True,
                            }
                        )

# =========================================================
# WRITE OUTPUT
# =========================================================

df = pd.DataFrame(events)
df.to_csv("ad_events.csv", index=False)

print(f"Generated {len(df):,} ad events")
