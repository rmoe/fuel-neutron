from neutron.db import model_base

from fuel_neutron.db import fuel_db # noqa


def get_metadata():
    return model_base.BASEV2.metadata
