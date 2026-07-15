"""created events

Revision ID: e0e5516b491a
Revises: 9ff023b1a38f
Create Date: 2026-03-28 12:39:38.794411        

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0e5516b491a'
down_revision: Union[str, Sequence[str], None] = '9ff023b1a38f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'Logs',
        sa.Column('messages', sa.String(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_Logs_id'), 'Logs', ['id'], unique=False)

    # create enum first
    auth_provider_enum = sa.Enum(
        'GOOGLE',
        'APPLE',
        'EMAIL',
        name='authprovider'
    )

    auth_provider_enum.create(op.get_bind(), checkfirst=True)

    # convert column from varchar → enum
    op.alter_column(
        'auth_accounts',
        'provider',
        existing_type=sa.VARCHAR(length=50),
        type_=auth_provider_enum,
        existing_nullable=False,
        postgresql_using="provider::authprovider"
    )

    op.create_index(
        'uix_provider_user',
        'auth_accounts',
        ['provider', 'user_id'],
        unique=True
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index('uix_provider_user', table_name='auth_accounts')

    op.alter_column(
        'auth_accounts',
        'provider',
        existing_type=sa.Enum(
            'GOOGLE',
            'APPLE',
            'EMAIL',
            name='authprovider'
        ),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False
    )

    sa.Enum(
        'GOOGLE',
        'APPLE',
        'EMAIL',
        name='authprovider'
    ).drop(op.get_bind(), checkfirst=True)

    op.drop_index(op.f('ix_Logs_id'), table_name='Logs')

    op.drop_table('Logs')