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

from generate_ad_creative import generate_ad_creative

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
BASE_VIEW_TO_CONVERSION = 0.001  # 1 conversion per 1K impressions without a click

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
creatives = []

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

                creative = generate_ad_creative()
                creatives.append(creative)  # for creative dim table

                # ----------------------------
                # Impression
                # ----------------------------
                impression_id = fake.uuid4()
                event_ts = session_start + timedelta(seconds=random.randint(0, 600))

                # reset click flag for each impression
                click_happened = False

                impression_event = {
                    "event_id": impression_id,
                    "session_id": session_id,
                    "user_id": user_id,
                    "ad_id": creative["ad_id"],
                    "ad_format": creative["ad_format"],
                    "creative_type": creative["creative_type"],
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
                    "revenue_usd": creative["base_cpm_usd"] / 1000,
                    "cost_usd": creative["base_cpm_usd"] / 1000,
                    "view_duration_ms": view_duration_ms("impression", placement),
                    "is_billable": True,
                    # other fields are null for impressions vs clicks vs conversions
                    "impression_id": impression_id,
                    "click_id": None,
                    "attribution_type": None,
                }

                events.append(impression_event)

                # ----------------------------
                # Click
                # ----------------------------
                click_probability = (
                    BASE_IMPRESSION_TO_CLICK
                    * placement["click_boost"]
                    * creative["click_boost"]
                )

                if random.random() < click_probability:
                    click_happened = True
                    click_id = fake.uuid4()
                    click_ts = event_ts + timedelta(seconds=random.randint(1, 15))
                    click_event = {
                        **impression_event,
                        # override impression fields for click event
                        "event_id": click_id,
                        "event_type": "click",
                        "event_timestamp": click_ts,
                        "revenue_usd": 0.0,
                        "cost_usd": round(random.uniform(0.05, 0.50), 2),
                        # other fields are null for impressions vs clicks vs conversions
                        "impression_id": impression_id,
                        "click_id": None,
                        "attribution_type": "click_through",
                    }

                    events.append(click_event)

                # ----------------------------
                # Conversion - either click-through or view-through
                # ----------------------------
                conversion_probability = (
                    BASE_CLICK_TO_CONVERSION
                    if click_happened
                    else BASE_VIEW_TO_CONVERSION
                )

                if random.random() < conversion_probability:
                    conversion_id = fake.uuid4()
                    conversion_ts = (
                        click_ts if click_happened else event_ts
                    ) + timedelta(minutes=random.randint(1, 60))

                    conversion_event = {
                        **impression_event,
                        "event_id": conversion_id,
                        "event_type": "conversion",
                        "event_timestamp": conversion_ts,
                        "revenue_usd": round(random.uniform(5, 150), 2),
                        "cost_usd": 0.0,
                        "impression_id": impression_id,
                        "click_id": click_id if click_happened else None,
                        "attribution_type": (
                            "click_through" if click_happened else "view_through"
                        ),
                    }

                    events.append(conversion_event)

# =========================================================
# WRITE OUTPUT
# =========================================================

df = pd.DataFrame(events)
df.to_csv("ad_events.csv", index=False)

print(f"Generated {len(df):,} ad events")

df_creatives = pd.DataFrame(creatives)
df_creatives.to_csv("ad_creatives.csv", index=False)
print(f"Generated {len(df_creatives):,} ad creatives")
