from .db import fuel_db
from neutron.plugins.common import constants
from oslo_config import cfg
from neutron.services import service_base
import os


class FuelPlugin(service_base.ServicePluginBase,
                 fuel_db.FuelDbMixin):
    """Implements Neutron-Fuel integration plugin."""

    supported_extension_aliases = ['fuel']

    def __init__(self):
        if not cfg.CONF.api_extensions_path:
            this = os.path.dirname(__file__)
            ext_path = os.path.sep.join([this, 'extensions'])
            cfg.CONF.set_override('api_extensions_path',
                                   ext_path)

    def get_plugin_type(self):
        return 'FUEL'

    def get_plugin_description(self):
        return "Neutron-Fuel integration manager plugin"
