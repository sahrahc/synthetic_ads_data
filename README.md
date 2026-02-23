
# Synthetic Netflix-Style Ads & Playback Data Generator

This repository contains a **deterministic, production-inspired synthetic data generator** for a **Netflix-style ad-supported streaming platform**.

It is designed for:
- Dimensional modeling (star schemas)
- dbt transformations
- Snowflake ingestion
- Ads revenue, trends, and retention analysis
- CTV / streaming–specific analytics (pre-roll, mid-roll, playback)

The goal is **realistic analytics behavior**, not toy data.

---

## 📦 What This Generates

The generator produces **five core datasets** that mirror a real streaming ads platform:

| File | Description |
|----|----|
| `users.csv` | User dimension (segments, geo, device, lifecycle) |
| `content.csv` | Movies & episodes with ad-relevant metadata |
| `campaigns.csv` | Advertiser campaigns, budgets, objectives |
| `playback_sessions.csv` | Viewing sessions (CTV-style playback) |
| `ad_events.csv` | Ad impressions, clicks, conversions |

All datasets are:
- Deterministic (same seed = same output)
- Referentially consistent
- Analytics-ready

---

## 🧠 Design Principles

### 1. Deterministic by default
All generators use a shared random seed:

SEED = 51

This ensures:
- Reproducible results
- Stable joins across tables
- Debuggable analytics
- CI-safe dbt tests

---

### 2. Separation of concerns

Each generator produces **one logical dataset**:
generate_users.py → dim_user
generate_content.py → dim_content / dim_series
generate_campaigns.py → dim_campaign
generate_playback_sessions.py → fact_playback_session
generate_ads_events.py → fact_ad_event

No generator mutates another dataset.

---

### 3. Enumerated domains
All categorical values live in a single file:
enums.py

This includes:
- Devices & OS
- Geo hierarchy
- Ad placements (Netflix-style)
- Event types

---

### 4. Streaming-native modeling
This is **not social ads data**.

The model reflects CTV realities:
- Playback sessions, not page views
- Pre-roll / mid-roll / post-roll ads
- Long view durations
- Fewer impressions, higher CPM
- Content context drives performance

---

## 🗂 Project Structure
synthetic_ads/
├── enums.py
├── generate_users.py
├── generate_content.py
├── generate_campaigns.py
├── generate_playback_sessions.py
├── generate_ads_events.py
├── requirements.txt
├── users.csv
├── content.csv
├── campaigns.csv
├── playback_sessions.csv
└── ad_events.csv

---

## 🔄 Data Model Overview

### Core join graph

users.user_id
↓
playback_sessions.user_id
↓
ad_events.session_id
↓
campaigns.campaign_id

playback_sessions.content_id → content.content_id


This enables:
- Revenue per viewing hour
- Ad load vs churn
- Mid-roll impact analysis
- Genre-based monetization
- Campaign pacing vs watch time

---

## 📊 Dataset Details

### Users (`users.csv`)
- User lifecycle dates
- Segments (`ad_supported`, `premium`, `kids`)
- Geo and primary device
- SCD-ready (`updated_at`)

Used for:
- Retention
- Cohorts
- Ad eligibility logic

---

### Content (`content.csv`)
- Movies and episodic content
- Genre and maturity rating
- Duration and release year
- Netflix-original flag

Used for:
- Brand safety
- CPM pricing
- Content-aware performance analysis

---

### Campaigns (`campaigns.csv`)
- Advertisers
- Objectives (`awareness`, `consideration`, `conversion`)
- Budgets and date ranges
- Bid strategy (`CPM`, `CPC`, `CPA`)

Used for:
- Revenue reporting
- ROAS
- Budget pacing

---

### Playback Sessions (`playback_sessions.csv`)
- Viewing sessions per user
- Session duration
- Content watched
- Device and geo context

Used for:
- Ad load normalization
- Churn analysis
- Binge behavior

---

### Ad Events (`ad_events.csv`)
- Impressions, clicks, conversions
- Netflix-style placements:
  - `pre_roll`
  - `mid_roll`
  - `post_roll`
  - `pause_screen`
  - `home_sponsorship`
- Revenue, cost, view duration
- Session-scoped

Used for:
- Funnel analysis
- Revenue attribution
- Placement performance

---

## ▶️ How to Run

### 1. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Generate all datasets

Run in this order (important):

python generate_users.py
python generate_content.py
python generate_campaigns.py
python generate_playback_sessions.py
python generate_ads_events.py

Each script writes a CSV to the project root.