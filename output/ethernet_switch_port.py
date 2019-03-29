from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# from  import vla_ns
# from  import static_ma_cs

# ============= import fields from other modules
# from  import ip_addresses
# from  import resource
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class OemField(base.CompositeField):
    """Oem field

       Oem extension object.
    """


class IPv6AddressCollectionField(rsd_lib_base.ReferenceableMemberField):

    oem = resource.OemField("Oem")

    address = base.Field("Address")
    """This is the IPv6 Address."""

    prefix_length = base.Field("PrefixLength")
    """This is the IPv6 Address Prefix Length."""

    address_origin = base.Field("AddressOrigin")
    """This indicates how the address was determined."""

    address_state = base.Field("AddressState")
    """The current state of this address as defined in RFC 4862."""


class IPv4AddressCollectionField(rsd_lib_base.ReferenceableMemberField):

    oem = resource.OemField("Oem")

    address = base.Field("Address")
    """This is the IPv4 Address."""

    subnet_mask = base.Field("SubnetMask")
    """This is the IPv4 Subnet mask."""

    address_origin = base.Field("AddressOrigin")
    """This indicates how the address was determined."""

    gateway = base.Field("Gateway")
    """This is the IPv4 gateway for this address."""


# ============================================


class NeighborInfoField(base.CompositeField):

    switch_id = base.Field("SwitchId")

    port_id = base.Field("PortId")

    cable_id = base.Field("CableId")


class LinksField(base.CompositeField):

    primary_vlan = base.Field(
        "PrimaryVLAN", adapter=rsd_lib_utils.get_resource_identity
    )

    switch = base.Field("Switch", adapter=rsd_lib_utils.get_resource_identity)

    member_of_port = base.Field(
        "MemberOfPort", adapter=rsd_lib_utils.get_resource_identity
    )

    port_members = base.Field(
        "PortMembers", adapter=utils.get_members_identities
    )

    active_ac_ls = base.Field(
        "ActiveACLs", adapter=utils.get_members_identities
    )


class EthernetSwitchPort(rsd_lib_base.ResourceBase):

    port_id = base.Field("PortId")
    """Switch port unique identifier."""

    link_type = base.Field("LinkType")
    """Type of port link"""

    operational_state = base.Field("OperationalState")
    """Port link operational state"""

    administrative_state = base.Field("AdministrativeState")
    """Port link state forced by user."""

    link_speed_mbps = base.Field(
        "LinkSpeedMbps", adapter=rsd_lib_utils.num_or_none
    )
    """Port speed"""

    neighbor_info = NeighborInfoField("NeighborInfo")
    """For Upstream port type this property provide information about neighbor
       switch (and switch port if available) connected to this port
    """

    neighbor_mac = base.Field("NeighborMAC")
    """For Downstream port type this property provide MAC address of NIC
       connected to this port.
    """

    frame_size = base.Field("FrameSize", adapter=rsd_lib_utils.num_or_none)
    """MAC frame size in bytes"""

    autosense = base.Field("Autosense", adapter=bool)
    """Indicates if the speed and duplex is automatically configured by the NIC
    """

    full_duplex = base.Field("FullDuplex", adapter=bool)
    """Indicates if port is in Full Duplex mode or not"""

    mac_address = base.Field("MACAddress")
    """MAC address of port."""

    i_pv4_addresses = ip_addresses.IPv4AddressCollectionField("IPv4Addresses")
    """Array of following IPv4 address"""

    i_pv6_addresses = ip_addresses.IPv6AddressCollectionField("IPv6Addresses")
    """Array of following IPv6 address"""

    port_class = base.Field("PortClass")
    """Port class"""

    port_mode = base.Field("PortMode")
    """Port working mode. The value shall correspond to the port class
       (especially to the logical port definition).
    """

    port_type = base.Field("PortType")
    """PortType"""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    links = LinksField("Links")

    @property
    @utils.cache_it
    def vla_ns(self):
        """Property to provide reference to `VLanNetworkInterfaceCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return v_lan_network_interface.VLanNetworkInterfaceCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "VLANs"),
            redfish_version=self.redfish_version,
        )

    @property
    @utils.cache_it
    def static_ma_cs(self):
        """Property to provide reference to `EthernetSwitchStaticMACCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return ethernet_switch_static_mac.EthernetSwitchStaticMACCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "StaticMACs"),
            redfish_version=self.redfish_version,
        )


class EthernetSwitchPortCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return EthernetSwitchPort
