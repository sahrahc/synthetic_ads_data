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
