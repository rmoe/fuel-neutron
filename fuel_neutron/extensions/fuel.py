from neutron.api.extensions import ExtensionDescriptor
from neutron.api import extensions
from neutron.api.v2 import attributes as attr
from neutron.api.v2 import base
from neutron.common import exceptions as nexception
from neutron import manager
from neutron.quota import resource_registry

class NicNotFound(nexception.NotFound):
    message = _("Nic %(nic_id)s could not be found.")

NICS = 'nics'
RESOURCE_ATTRIBUTE_MAP = {
    NICS: {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'primary_key': True
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
            'default': '',
            'validate': {
                'type:name_not_default': attr.NAME_MAX_LEN
            }
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'required_by_policy': True,
            'validate': {'type:string': attr.TENANT_ID_MAX_LEN},
            'is_visible': True
        },
    }
}


class Fuel(ExtensionDescriptor):

    @classmethod
    def get_name(self):
        return 'Fuel Integration'

    @classmethod
    def get_alias(self):
        return 'fuel'

    @classmethod
    def get_description(self):
        return 'Integrates Neutron with Fuel'

    @classmethod
    def get_updated(self):
        return '2016-03-15T09:00:00-08:00'

    @classmethod
    def get_resources(cls):
        """Returns Ext Resources."""
        my_plurals = [(key, key[:-1]) for key in RESOURCE_ATTRIBUTE_MAP.keys()]
        attr.PLURALS.update(dict(my_plurals))
        exts = []
        plugin = manager.NeutronManager.get_service_plugins()['FUEL']
        for resource_name in ['nic']:
            collection_name = resource_name.replace('_', '-') + "s"
            params = RESOURCE_ATTRIBUTE_MAP.get(resource_name + "s", dict())
            resource_registry.register_resource_by_name(resource_name)
            controller = base.create_resource(collection_name,
                                              resource_name,
                                              plugin, params, allow_bulk=True,
                                              allow_pagination=True,
                                              allow_sorting=True)

            ex = extensions.ResourceExtension(collection_name,
                                              controller,
                                              path_prefix='fuel',
                                              attr_map=params)
            exts.append(ex)

        return exts

    def update_attributes_map(self, attributes):
        super(Fuel, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP)
