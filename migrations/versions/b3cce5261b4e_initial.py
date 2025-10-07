"""initial

Revision ID: b3cce5261b4e
Revises: c10311e446a8
Create Date: 2025-07-11 14:38:42.017788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3cce5261b4e'
down_revision = 'c10311e446a8'
branch_labels = None
depends_on = None


def upgrade():
    # ✅ Fixed: Added server_default for quantity
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('quantity', sa.Integer(), nullable=False, server_default="1")
        )


def downgrade():
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.drop_column('quantity')
