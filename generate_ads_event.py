import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

###############################################
# # Generate synthetic ad events data
# Analytics validation
# Ads modeling
# Retention studies
# ML feature testing
###############################################

fake = Faker()

# stable randomness for regression testing and reproducible dashboards,
#    same retention curves and funnel counts
random.seed(51)

N_USERS = 10000
DAYS = 30

users = [f"user_{i}" for i in range(N_USERS)]
start_date = datetime(2026, 1, 1)

events = []

for user in users:
    # explicit, exponentially decaying probability distribution over days
    # increase for slower churn
    weights = [0.6**d for d in range(DAYS)]

    # how many days the users stays active. Most users churn quickly;
    # long-tail power users for a realistic retention curve
    active_days = random.choices(range(DAYS), weights=weights)[0]

    for day in range(active_days):
        event_ts = start_date + timedelta(days=day)
        events.append(
            {
                "event_id": fake.uuid4(),
                "user_id": user,
                "ad_id": f"ad_{random.randint(1, 200)}",
                "campaign_id": f"camp_{random.randint(1, 20)}",
                "event_type": "impression",
                "event_timestamp": event_ts,
                "revenue_usd": 0.0,
            }
        )

        # 9% click-through rate and 1% conversion rate for a realistic funnel
        if random.random() < 0.09:
            events.append(
                {
                    "event_id": fake.uuid4(),
                    "user_id": user,
                    "ad_id": f"ad_{random.randint(1, 200)}",
                    "campaign_id": f"camp_{random.randint(1, 20)}",
                    "event_type": "click",
                    "event_timestamp": event_ts,
                    "revenue_usd": 0.0,
                }
            )

        if random.random() < 0.01:
            events.append(
                {
                    "event_id": fake.uuid4(),
                    "user_id": user,
                    "ad_id": f"ad_{random.randint(1, 200)}",
                    "campaign_id": f"camp_{random.randint(1, 20)}",
                    "event_type": "conversion",
                    "event_timestamp": event_ts,
                    "revenue_usd": round(random.uniform(1, 50), 2),
                }
            )

df = pd.DataFrame(events)
df.to_csv("ad_events.csv", index=False)
