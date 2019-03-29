from rsd_lib import base as rsd_lib_base


from rsd_lib import utils as rsd_lib_utils


class EthernetSwitchStaticMAC(rsd_lib_base.ResourceBase):
    """EthernetSwitchStaticMAC resource class

       A Ethernet Switch ACL represents Access Control List for switch.
    """

    vlan_id = base.Field("VLANId", adapter=rsd_lib_utils.num_or_none)

    mac_address = base.Field("MACAddress")


class EthernetSwitchStaticMACCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return EthernetSwitchStaticMAC
