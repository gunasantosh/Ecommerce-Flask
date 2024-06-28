"""Added Category model

Revision ID: 61abfe5ae337
Revises: 
Create Date: 2024-06-28 08:08:13.538640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61abfe5ae337'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
