# generate_content.py

import random
import pandas as pd
from faker import Faker
from datetime import datetime

from enums import (
    GENRES,
)

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

N_MOVIES = 300
N_SERIES = 200
MAX_SEASONS_PER_SERIES = 6
MAX_EPISODES_PER_SEASON = 12

RELEASE_YEARS = list(range(1995, 2026))

GENRE_WEIGHTS = [0.12, 0.09, 0.18, 0.09, 0.04, 0.10, 0.05, 0.09, 0.10, 0.07, 0.05, 0.02]

MATURITY_RATINGS = ["G", "PG", "PG-13", "TV-14", "TV-MA"]
RATING_WEIGHTS = [0.08, 0.18, 0.24, 0.28, 0.22]

# =========================================================
# GENERATE MOVIES
# =========================================================

content = []

for i in range(1, N_MOVIES + 1):
    genre = random.choices(GENRES, GENRE_WEIGHTS)[0]
    maturity = random.choices(MATURITY_RATINGS, RATING_WEIGHTS)[0]

    duration = random.randint(75, 160)
    release_year = random.choice(RELEASE_YEARS)

    content.append(
        {
            "content_id": f"movie_{i}",
            "content_type": "movie",
            "title": fake.catch_phrase(),
            "series_id": None,
            "season_number": None,
            "episode_number": None,
            "genre": genre,
            "maturity_rating": maturity,
            "duration_minutes": duration,
            "release_year": release_year,
            "is_original": random.random() < 0.6,
            "created_at": datetime.now(),
        }
    )

# =========================================================
# GENERATE SERIES + EPISODES
# =========================================================

series_counter = 1
episode_counter = 1

for s in range(1, N_SERIES + 1):
    series_id = f"series_{series_counter}"
    series_counter += 1

    genre = random.choices(GENRES, GENRE_WEIGHTS)[0]
    maturity = random.choices(MATURITY_RATINGS, RATING_WEIGHTS)[0]
    release_year = random.choice(RELEASE_YEARS)

    seasons = random.randint(1, MAX_SEASONS_PER_SERIES)

    for season in range(1, seasons + 1):
        episodes = random.randint(4, MAX_EPISODES_PER_SEASON)

        for ep in range(1, episodes + 1):
            duration = random.randint(18, 65)

            content.append(
                {
                    "content_id": f"episode_{episode_counter}",
                    "content_type": "episode",
                    "title": f"{fake.catch_phrase()} – S{season}E{ep}",
                    "series_id": series_id,
                    "season_number": season,
                    "episode_number": ep,
                    "genre": genre,
                    "maturity_rating": maturity,
                    "duration_minutes": duration,
                    "release_year": release_year,
                    "is_original": random.random() < 0.7,
                    "created_at": datetime.now(),
                }
            )

            episode_counter += 1

# =========================================================
# WRITE OUTPUT
# =========================================================

df = pd.DataFrame(content)
df.to_csv("content.csv", index=False)

print(f"Generated {len(df):,} content rows")
