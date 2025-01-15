"""
Add User model

Revision ID: 5e50f76d9599
Revises: 937d59e29f3e
Create Date: 2025-01-10 07:51:15.566513

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5e50f76d9599"
down_revision: str | None = "937d59e29f3e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("users",
    sa.Column("email", sa.String(length=255), nullable=False),
    sa.Column("password", sa.String(length=255), nullable=False),
    sa.Column("first_name", sa.String(length=50), nullable=True),
    sa.Column("last_name", sa.String(length=50), nullable=True),
    sa.Column("is_active", sa.Boolean(), nullable=True),
    sa.Column("is_superuser", sa.Boolean(), nullable=True),
    sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
    sa.Column("created", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("updated", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_created"), "users", ["created"], unique=False)
    op.create_index(op.f("ix_user_email"), "users", ["email"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_email"), table_name="users")
    op.drop_index(op.f("ix_user_created"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
