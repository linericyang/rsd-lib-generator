from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base


from rsd_lib import utils as rsd_lib_utils


class IntelRackScaleField(base.CompositeField):

    pc_ie_connection_id = base.Field("PCIeConnectionId")
    """An array of references to the PCIe connection identifiers (e.g. cable
       ID).
    """


class LinksField(base.CompositeField):

    associated_endpoints = base.Field(
        "AssociatedEndpoints", adapter=utils.get_members_identities
    )
    """An array of references to the endpoints that connect to the switch
       through this port.
    """

    connected_switches = base.Field(
        "ConnectedSwitches", adapter=utils.get_members_identities
    )
    """An array of references to the switches that connect to the switch
       through this port.
    """

    connected_switch_ports = base.Field(
        "ConnectedSwitchPorts", adapter=utils.get_members_identities
    )
    """An array of references to the ports that connect to the switch through
       this port.
    """


class OemField(base.CompositeField):

    intel_rackscale = IntelRackScaleField("Intel_RackScale")
    """Intel Rack Scale Design specific properties."""


class Port(rsd_lib_base.ResourceBase):
    """Port resource class

       Port contains properties describing a port of a switch.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    port_id = base.Field("PortId")
    """This is the label of this port on the physical switch package."""

    port_protocol = base.Field("PortProtocol")
    """The protocol being sent over this port."""

    port_type = base.Field("PortType")
    """This is the type of this port."""

    current_speed_gbps = base.Field(
        "CurrentSpeedGbps", adapter=rsd_lib_utils.num_or_none
    )
    """The current speed of this port."""

    max_speed_gbps = base.Field(
        "MaxSpeedGbps", adapter=rsd_lib_utils.num_or_none
    )
    """The maximum speed of this port as currently configured."""

    width = base.Field("Width", adapter=rsd_lib_utils.num_or_none)
    """The number of lanes, phys, or other physical transport links that this
       port contains.
    """

    links = LinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """

    oem = OemField("Oem")
    """Oem specific properties."""


# TODO(linyang): Add Action Field


class PortCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return Port
