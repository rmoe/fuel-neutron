import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import exc as sa_exc
from neutron.db import model_base
from neutron.api.v2 import attributes as attr
from neutron.db import common_db_mixin

from fuel_neutron.extensions import fuel as ext_fuel

class Nic(model_base.BASEV2, model_base.HasId):
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))


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
        n = nic[nic]
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
