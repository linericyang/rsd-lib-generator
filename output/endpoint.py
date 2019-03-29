from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import resource
# from  import redundancy
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module

class OemField(base.CompositeField):
    """Oem field

       Oem extension object.
    """



class ResourceField(base.CompositeField):




class RedundancyCollectionField(rsd_lib_base.ReferenceableMemberField):
    """Redundancy field

       This is the common redundancy definition and structure used in other
       Redfish schemas.
    """



class IdentifierCollectionField(rsd_lib_base.ReferenceableMemberField):


    durable_name = base.Field("DurableName")
    """This indicates the world wide, persistent name of the resource."""

    durable_name_format = base.Field("DurableNameFormat")
    """This represents the format of the DurableName property."""


# ============================================


class LinksField(base.CompositeField):


    mutually_exclusive_endpoints = base.Field("MutuallyExclusiveEndpoints", adapter=utils.get_members_identities)
    """An array of references to the endpoints that may not be used in zones
       if this endpoint is used in a zone.
    """

    ports = base.Field("Ports", adapter=utils.get_members_identities)
    """An array of references to the the physical ports associated with this
       endpoint.
    """


class PciIdField(base.CompositeField):


    device_id = base.Field("DeviceId")
    """The Device ID of this PCIe function."""

    vendor_id = base.Field("VendorId")
    """The Vendor ID of this PCIe function."""

    subsystem_id = base.Field("SubsystemId")
    """The Subsystem ID of this PCIe function."""

    subsystem_vendor_id = base.Field("SubsystemVendorId")
    """The Subsystem Vendor ID of this PCIe function."""



class ConnectedEntityCollectionField(rsd_lib_base.ReferenceableMemberField):
    """ConnectedEntity field

       Represents a remote resource that is connected to the network
       accessible to this endpoint.
    """


    entity_type = base.Field("EntityType")
    """The type of the connected entity."""

    entity_role = base.Field("EntityRole")
    """The role of the connected entity."""

    entity_pci_id = PciIdField("EntityPciId")
    """The PCI ID of the connected entity."""

    pci_function_number = base.Field("PciFunctionNumber", adapter=rsd_lib_utils.num_or_none)
    """The PCI ID of the connected entity."""

    pci_class_code = base.Field("PciClassCode")
    """The Class Code and Subclass code of this PCIe function."""

    identifiers = resource.IdentifierCollectionField("Identifiers")
    """Identifiers for the remote entity."""

    oem = resource.OemField("Oem")


    entity_link = resource.ResourceField("EntityLink")
    """A link to the associated entity."""


class Endpoint(rsd_lib_base.ResourceBase):
    """Endpoint resource class

       This is the schema definition for the Endpoint resource. It represents
       the properties of an entity that sends or receives protocol defined
       messages over a transport.
    """


    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    endpoint_protocol = base.Field("EndpointProtocol")
    """The protocol supported by this endpoint."""

    connected_entities = ConnectedEntityCollectionField("ConnectedEntities")
    """All the entities connected to this endpoint."""

    identifiers = resource.IdentifierCollectionField("Identifiers")
    """Identifiers for this endpoint"""

    pci_id = PciIdField("PciId")
    """The PCI ID of the endpoint."""

    host_reservation_memory_bytes = base.Field("HostReservationMemoryBytes", adapter=rsd_lib_utils.num_or_none)
    """The amount of memory in Bytes that the Host should allocate to connect
       to this endpoint.
    """

    links = LinksField("Links")
    """The links object contains the links to other resources that are related
       to this resource.
    """


    redundancy = redundancy.RedundancyCollectionField("Redundancy")
    """Redundancy information for the lower level endpoints supporting this
       endpoint
    """

# TODO(linyang): Add Action Field

class EndpointCollection(rsd_lib_base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Endpoint
