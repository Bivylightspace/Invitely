import base64
import io
import re
from typing import Any

from supabase import create_client

from api.utils.config import settings
from dicebear.avatar import DAvatar


def _normalize_seed(seed: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", seed.strip().lower())
    return safe_name[:128].rstrip("_") or "avatar"


def _extract_avatar_bytes(avatar: Any) -> bytes:
    if hasattr(avatar, "to_data_uri"):
        data_uri = avatar.to_data_uri()
        if isinstance(data_uri, str) and data_uri.startswith("data:image/svg+xml;base64,"):
            return base64.b64decode(data_uri.split(",", 1)[1])
        return str(data_uri).encode("utf-8")

    if hasattr(avatar, "to_string"):
        return avatar.to_string().encode("utf-8")

    if hasattr(avatar, "to_svg"):
        return avatar.to_svg().encode("utf-8")

    if hasattr(avatar, "text"):
        return avatar.text().encode("utf-8")

    raise RuntimeError("Unable to extract avatar SVG bytes from the DiceBear avatar object.")


def upload_default_avatar(seed: str) -> dict:
    supabase_service_key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
    if not settings.SUPABASE_URL or not supabase_service_key:
        raise RuntimeError(
            "Supabase configuration is not available. Set SUPABASE_URL and SUPABASE_SERVICE_KEY or SUPABASE_KEY."
        )

    avatar = DAvatar("lorelei", seed=seed)
    avatar_bytes = _extract_avatar_bytes(avatar)
    storage_path = f"{_normalize_seed(seed)}.svg"
    target_bucket = settings.AVATAR_BUCKET_NAME or settings.BUCKET_NAME

    supabase_client = create_client(settings.SUPABASE_URL, supabase_service_key)
    upload_result = supabase_client.storage.from_(target_bucket).upload(
        storage_path,
        avatar_bytes,
        {"content-type": "image/svg+xml", "upsert": "true"},
    )

    error = None
    if isinstance(upload_result, dict):
        error = upload_result.get("error")
    elif hasattr(upload_result, "get"):
        error = upload_result.get("error")
    elif hasattr(upload_result, "error"):
        error = getattr(upload_result, "error")

    if error:
        raise RuntimeError(f"Supabase upload failed: {error}")

    return {"bucket": target_bucket, "path": storage_path}
