"""add_nics_table

Revision ID: f6e871ee0838
Revises: 4b552cba3da7
Create Date: 2016-03-17 14:10:54.664354

"""

# revision identifiers, used by Alembic.
revision = 'f6e871ee0838'
down_revision = '4b552cba3da7'

from alembic import op
import sqlalchemy as sa

from neutron.api.v2 import attributes as attr


def upgrade():
    op.create_table(
        'fuel_nics',
        sa.Column('tenant_id', sa.String(length=attr.TENANT_ID_MAX_LEN),
                  nullable=True, index=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=attr.NAME_MAX_LEN),
                  nullable=True),

        sa.Column('mac', sa.String(32)),
        sa.Column('if_type', sa.String(64)),
        sa.Column('interface_properties', sa.Text),
        sa.Column('current_speed', sa.Integer),
        sa.Column('max_speed', sa.Integer),
        sa.Column('driver', sa.Text),
        sa.Column('bus_info', sa.Text),
        sa.Column('pxe', sa.Boolean),
        sa.Column('offloading_modes', sa.Text),
        sa.Column('provider', sa.String(25)),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'fuel_nics_slaves',
        sa.Column('parent', sa.String(36)),
        sa.Column('slave', sa.String(36)),
        sa.ForeignKeyConstraint(
            ['parent'], ['fuel_nics.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['slave'], ['fuel_nics.id'], ondelete='CASCADE'
        )
    )
