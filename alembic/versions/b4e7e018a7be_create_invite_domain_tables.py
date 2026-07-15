"""create invite domain tables

Revision ID: b4e7e018a7be
Revises: 9ff023b1a38f
Create Date: 2026-06-17 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "b4e7e018a7be"
down_revision = "9ff023b1a38f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.String(length=255), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("event_date", sa.String(length=80), nullable=True),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("upload_path", sa.String(length=500), nullable=True),
        sa.Column("host_id", sa.String(length=255), sa.ForeignKey("users.id"), nullable=False),
    )

    op.create_table(
        "guests",
        sa.Column("id", sa.String(length=255), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("event_id", sa.String(length=255), sa.ForeignKey("events.id"), nullable=False),
    )

    op.create_table(
        "invite_links",
        sa.Column("id", sa.String(length=255), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("token", sa.String(length=255), unique=True, nullable=False),
        sa.Column("url", sa.String(length=500), nullable=True),
        sa.Column("event_id", sa.String(length=255), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("guest_id", sa.String(length=255), sa.ForeignKey("guests.id"), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    op.create_table(
        "rsvps",
        sa.Column("id", sa.String(length=255), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("guest_id", sa.String(length=255), sa.ForeignKey("guests.id"), nullable=False),
        sa.Column("invite_link_id", sa.String(length=255), sa.ForeignKey("invite_links.id"), nullable=False),
        sa.Column("status", sa.Enum("attending", "not_attending", name="rsvpstatus"), nullable=False),
        sa.Column("response_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("rsvps")
    op.drop_table("invite_links")
    op.drop_table("guests")
    op.drop_table("events")
