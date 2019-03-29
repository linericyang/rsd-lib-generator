from sushy.resources import base


from rsd_lib import base as rsd_lib_base


class IntelRackScaleField(base.CompositeField):

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    tagged = base.Field("Tagged", adapter=bool)
    """This indicates if VLAN is tagged (as defined in IEEE 802.1Q)."""


class OemField(base.CompositeField):

    intel_rackscale = IntelRackScaleField("Intel_RackScale")
    """Intel Rack Scale Design specific properties."""


class VLanNetworkInterface(rsd_lib_base.ResourceBase):
    """VLanNetworkInterface resource class

       This resource contains information for a Virtual LAN (VLAN) network
       instance available on a manager, system or other device.
    """

    vlan_enable = base.Field("VLANEnable", adapter=bool)
    """This indicates if this VLAN is enabled."""

    vlan_id = base.Field("VLANId")
    """This indicates the VLAN identifier for this VLAN."""

    oem = OemField("Oem")
    """Oem specific properties."""


class VLanNetworkInterfaceCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return VLanNetworkInterface
