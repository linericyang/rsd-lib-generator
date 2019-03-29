from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# from  import rules


class LinksField(base.CompositeField):

    bound_ports = base.Field(
        "BoundPorts", adapter=utils.get_members_identities
    )


class EthernetSwitchACL(rsd_lib_base.ResourceBase):
    """EthernetSwitchACL resource class

       A Ethernet Switch ACL represents Access Control List for switch.
    """

    links = LinksField("Links")

    # TODO(linyang): Add Action Field

    @property
    @utils.cache_it
    def rules(self):
        """Property to provide reference to `EthernetSwitchACLRuleCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return ethernet_switch_acl_rule.EthernetSwitchACLRuleCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Rules"),
            redfish_version=self.redfish_version,
        )


class EthernetSwitchACLCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return EthernetSwitchACL
