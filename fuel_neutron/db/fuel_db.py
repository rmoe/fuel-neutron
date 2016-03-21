import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import exc as sa_exc
from oslo_utils import uuidutils
from neutron.db import common_db_mixin
from neutron.db import model_base
from neutron.api.v2 import attributes as attr

from fuel_neutron.extensions import fuel as ext_fuel


fuel_nic_slaves = Table(
    'fuel_nics_slaves',
    model_base.BASEV2.metadata,
    Column('parent', String(64),
           ForeignKey('fuel_nics.id', ondelete='CASCADE')),
    Column('slave', String(64),
           ForeignKey('fuel_nics.id', ondelete='CASCADE'))
)

class Nic(model_base.BASEV2, model_base.HasId, model_base.HasTenant):
    __tablename__ = 'fuel_nics'

    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    mac = sa.Column(sa.String(32))
    if_type = sa.Column(sa.String(64))
    slaves = orm.relationship(
        'Nic',
        secondary='fuel_nics_slaves',
        primaryjoin='fuel_nics.c.id==fuel_nics_slaves.c.parent',
        secondaryjoin='fuel_nics.c.id==fuel_nics_slaves.c.slave',
        backref='parent_nic'
    )
    interface_properties = sa.Column(sa.Text)
    current_speed = sa.Column(sa.Integer)
    max_speed = sa.Column(sa.Integer)
    driver = sa.Column(sa.Text)
    bus_info = sa.Column(sa.Text)
    pxe = sa.Column(sa.Boolean)
    offloading_modes = sa.Column(sa.Text)
    provider = sa.Column(sa.String(25))


class FuelDbMixin(common_db_mixin.CommonDbMixin):

    """Class to support Fuel-related models."""

    def _get_nic(self, context, nic_id):
        try:
            return self._get_by_id(context, Nic, nic_id)
        except sa_exc.NoResultFound:
            raise ext_fuel.NicNotFound(nic_id=nic_id)

    def _make_nic_dict(self, nic_db, fields=None):
        res = {'id': nic_db['id'],
               'name': nic_db['name']
        }
        return self._fields(res, fields)

    def create_nic(self, context, nic):
        n = nic['nic']
        with context.session.begin(subtransactions=True):
            nic_db = Nic(id=uuidutils.generate_uuid(),
                           name=n['name'])

            context.session.add(nic_db)
        return self._make_nic_dict(nic_db)

    def update_nic(self, context, nic_id, nic):
        n = nic['nic']
        with context.session.begin(subtransactions=True):
            nic_db = self._get_nic(context, nic_id)
            nic_db.update(fl)
        return self._make_nic_dict(nic_db)

    def get_nic(self, context, nic_id, fields=None):
        nic_db = self._get_nic(context, nic_id)
        return self._make_nic_dict(nic_db, fields)

    def delete_nic(self, context, nic_id):
        with context.session.begin(subtransactions=True):
            nic_db = self._get_nic(context, nic_id)
            context.session.delete(nic_db)

    def get_nics(self, context, filters=None, fields=None,
                    sorts=None, limit=None, marker=None, page_reverse=False):
        return self._get_collection(context, Nic, self._make_nic_dict,
                                    filters=filters, fields=fields,
                                    sorts=sorts, limit=limit,
                                    marker_obj=marker,
                                    page_reverse=page_reverse)
