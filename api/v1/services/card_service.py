from typing import Any


def render_template_card(template_id: str, metadata: dict[str, Any]) -> str:
    """Placeholder for server-side card generation logic.

    Returns a storage path, URL, or asset identifier for the generated card.
    """
    # Future work: render a Pillow/PDF-based invite card, store to Supabase or S3.
    return f"template-card:{template_id}"
