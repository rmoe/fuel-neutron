"""empty message

Revision ID: 27088071cca7
Revises: 
Create Date: 2016-03-16 15:21:30.462745

"""

# revision identifiers, used by Alembic.
revision = '27088071cca7'
down_revision = None 
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'nics',
        sa.Column('id', sa.String(36)),
        sa.Column('name', sa.String(255)),
    )


def downgrade():
    pass
