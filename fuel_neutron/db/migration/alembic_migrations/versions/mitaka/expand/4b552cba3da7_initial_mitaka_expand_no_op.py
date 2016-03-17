"""Initial Mitaka expand no-op

Revision ID: 4b552cba3da7
Revises: eed0e74f8b87
Create Date: 2016-03-17 13:36:48.194078

"""
from neutron.db.migration import cli

# revision identifiers, used by Alembic.
revision = '4b552cba3da7'
down_revision = 'start_fuel'
branch_labels = (cli.EXPAND_BRANCH, )

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass
