"""Initial model setting

Revision ID: 9ced55c60fcb
Revises:
Create Date: 2024-05-02 17:08:17.954991

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ced55c60fcb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_users_social_id", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", mysql.VARCHAR(length=36), nullable=False),
        sa.Column("social_id", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("provider", mysql.VARCHAR(length=50), nullable=False),
        sa.Column("role", mysql.ENUM("admin", "user"), nullable=True),
        sa.Column("nickname", mysql.VARCHAR(length=100), nullable=True),
        sa.Column("deleted_at", mysql.DATETIME(), nullable=True),
        sa.Column("created_at", mysql.DATETIME(), nullable=False),
        sa.Column("updated_at", mysql.DATETIME(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("ix_users_social_id", "users", ["social_id"], unique=False)
    # ### end Alembic commands ###