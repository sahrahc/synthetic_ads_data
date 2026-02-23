# generate_campaigns.py

import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# =========================================================
# STABLE RANDOMNESS
# =========================================================

SEED = 42
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

# =========================================================
# PARAMETERS
# =========================================================

N_CAMPAIGNS = 20
START_DATE = datetime(2024, 12, 1)
END_DATE = datetime(2025, 3, 31)

OBJECTIVES = ["awareness", "consideration", "conversion"]
OBJECTIVE_WEIGHTS = [0.4, 0.35, 0.25]

BID_STRATEGIES = {
    "awareness": "CPM",
    "consideration": "CPC",
    "conversion": "CPA",
}

# =========================================================
# HELPERS
# =========================================================


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


# =========================================================
# GENERATE CAMPAIGNS
# =========================================================

campaigns = []

for i in range(N_CAMPAIGNS):
    campaign_id = f"camp_{i+1}"
    advertiser_id = f"adv_{random.randint(1, 10)}"

    objective = random.choices(OBJECTIVES, OBJECTIVE_WEIGHTS)[0]
    bid_strategy = BID_STRATEGIES[objective]

    start_date = random_date(START_DATE, END_DATE - timedelta(days=30))
    end_date = start_date + timedelta(days=random.randint(14, 60))

    daily_budget = round(random.uniform(500, 25_000), 2)

    campaigns.append(
        {
            "campaign_id": campaign_id,
            "advertiser_id": advertiser_id,
            "campaign_name": fake.catch_phrase(),
            "objective": objective,
            "bid_strategy": bid_strategy,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
            "daily_budget_usd": daily_budget,
            "total_budget_usd": round(daily_budget * (end_date - start_date).days, 2),
            "created_at": start_date,
            "updated_at": end_date,
        }
    )

# =========================================================
# WRITE OUTPUT
# =========================================================

df = pd.DataFrame(campaigns)
df.to_csv("campaigns.csv", index=False)

print(f"Generated {len(df):,} campaigns")
