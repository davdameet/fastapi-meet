"""create posts table

Revision ID: 59d36ab4802f
Revises: 
Create Date: 2022-08-16 18:40:44.495506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59d36ab4802f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("title",sa.String(),nullable=False),sa.Column("content",sa.String(),nullable=False))
def downgrade() -> None:
    op.drop_table("posts")
