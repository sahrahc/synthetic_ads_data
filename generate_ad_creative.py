import random
import uuid

from enums import AD_FORMATS, CREATIVE_TYPES


def generate_ad_creative():
    """
    Generate a Netflix-style ad creative with format and creative type.

    Returns a dict suitable for embedding in ad event rows.
    """

    ad_format = random.choice(list(AD_FORMATS.keys()))
    creative_type = random.choice(list(CREATIVE_TYPES.keys()))

    format_meta = AD_FORMATS[ad_format]
    creative_meta = CREATIVE_TYPES[creative_type]

    duration_sec = random.choice(format_meta["durations_sec"])

    ad_id = f"ad_{uuid.uuid4().hex[:10]}"

    return {
        "ad_id": ad_id,
        "ad_format": ad_format,  # video / bumper / pause_display
        "creative_type": creative_type,  # standard_video / interactive_qr
        "duration_seconds": duration_sec,
        "base_cpm_usd": format_meta["base_cpm"],
        "click_boost": creative_meta["click_boost"],
        "is_interactive": creative_type == "interactive_qr",
    }
