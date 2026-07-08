import re
from urllib.parse import quote_plus


def _normalize_seed(seed: str) -> str:
    """
    Cleans and standardizes the user seed to prevent url breakdown 
    and maintain consistent lowercase formats.
    """
    safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", seed.strip().lower())
    return safe_name[:128].rstrip("_") or "avatar"


def get_permanent_avatar_link(seed: str, style: str = "lorelei") -> dict:
    """
    Takes a unique identifier (like a username or user ID), normalizes it, 
    and constructs a permanent, non-expiring public DiceBear CDN image URL.
    """
    clean_seed = _normalize_seed(seed)
    url_safe_seed = quote_plus(clean_seed)
    avatar_url = f"https://api.dicebear.com/10.x/{style}/svg?seed={url_safe_seed}"
    
    return {
        "seed": clean_seed,
        "style": style,
        "avatar_url": avatar_url
    }
