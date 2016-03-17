"""Initial Mitaka no-op

Revision ID: eed0e74f8b87
Revises: start_fuel
Create Date: 2016-03-17 13:35:00.435441

"""

from neutron.db.migration import cli

# revision identifiers, used by Alembic.
revision = 'eed0e74f8b87'
down_revision = 'start_fuel'
branch_labels = (cli.CONTRACT_BRANCH,)

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass
