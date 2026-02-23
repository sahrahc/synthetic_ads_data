# enums.py

# =========================================================
# DEVICE & OS
# =========================================================

DEVICE_TYPES = ["mobile", "desktop", "tablet", "tv"]

OS_BY_DEVICE = {
    "mobile": ["iOS", "Android"],
    "tablet": ["iOS", "Android"],
    "desktop": ["macOS", "Windows", "Linux"],
    "tv": ["tvOS", "Android TV", "Roku"],
}

# =========================================================
# NETFLIX-STYLE PLACEMENTS (CTV / STREAMING)
# =========================================================

PLACEMENTS = [
    {
        "surface": "player",
        "placement": "pre_roll",
        "position": "before_content",
        "click_boost": 0.8,
        "view_boost": 1.4,
    },
    {
        "surface": "player",
        "placement": "mid_roll",
        "position": "during_content",
        "click_boost": 0.6,
        "view_boost": 1.6,
    },
    {
        "surface": "player",
        "placement": "post_roll",
        "position": "after_content",
        "click_boost": 0.3,
        "view_boost": 1.2,
    },
    {
        "surface": "ui",
        "placement": "pause_screen",
        "position": "overlay",
        "click_boost": 1.2,
        "view_boost": 1.1,
    },
    {
        "surface": "ui",
        "placement": "home_sponsorship",
        "position": "featured_row",
        "click_boost": 1.5,
        "view_boost": 1.0,
    },
]

# =========================================================
# GEO HIERARCHY
# =========================================================

GEO_HIERARCHY = {
    "US": {
        "CA": ["San Francisco", "Los Angeles"],
        "NY": ["New York"],
        "WA": ["Seattle"],
    },
    "CA": {"ON": ["Toronto"], "BC": ["Vancouver"]},
    "UK": {"ENG": ["London"], "SCT": ["Edinburgh"]},
}

# =========================================================
# EVENT TYPES
# =========================================================

EVENT_TYPES = ["impression", "click", "conversion"]

# =========================================================
# CONTENT GENRES
# =========================================================

GENRES = [
    "Action",
    "Comedy",
    "Drama",
    "Family",
    "Horror",
    "Kids",
    "Sci-Fi",
    "Romance",
    "Documentary",
    "Thriller",
    "Animation",
    "Fantasy",
]

# =========================================================
# CTV AD FORMATS & CREATIVE TYPES
# =========================================================

AD_FORMATS = {
    "video": {"durations_sec": [15, 30, 45, 60], "base_cpm": 35.0},
    "bumper": {"durations_sec": [6], "base_cpm": 25.0},
    "pause_display": {"durations_sec": [0], "base_cpm": 18.0},
    "ui_sponsorship": {"durations_sec": [0], "base_cpm": 22.0},
}

CREATIVE_TYPES = {
    "standard_video": {"click_boost": 1.0},
    "interactive_qr": {"click_boost": 1.6},
    "brand_slate": {"click_boost": 0.6},
    "sponsored_title_card": {"click_boost": 1.2},
}
