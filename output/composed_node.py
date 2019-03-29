from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import computer_system
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class BootField(base.CompositeField):
    """Boot field

       This object contains the boot information for the current resource.
    """

    boot_source_override_target = base.Field("BootSourceOverrideTarget")
    """The current boot source to be used at next boot instead of the normal
       boot device, if BootSourceOverrideEnabled is true.
    """

    boot_source_override_enabled = base.Field("BootSourceOverrideEnabled")
    """Describes the state of the Boot Source Override feature"""

    uefi_target_boot_source_override = base.Field(
        "UefiTargetBootSourceOverride"
    )
    """This property is the UEFI Device Path of the device to boot from when
       BootSourceOverrideSupported is UefiTarget.
    """

    boot_source_override_mode = base.Field("BootSourceOverrideMode")
    """The BIOS Boot Mode (either Legacy or UEFI) to be used when
       BootSourceOverrideTarget boot source is booted from.
    """


class ProcessorSummaryField(base.CompositeField):
    """ProcessorSummary field

       This object describes the central processors of the system in general
       detail.
    """

    count = base.Field("Count", adapter=rsd_lib_utils.num_or_none)
    """The number of processors in the system."""

    model = base.Field("Model")
    """The processor model for the primary or majority of processors in this
       system.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """


class MemorySummaryField(base.CompositeField):
    """MemorySummary field

       This object describes the memory of the system in general detail.
    """

    total_system_memory_gi_b = base.Field(
        "TotalSystemMemoryGiB", adapter=rsd_lib_utils.num_or_none
    )
    """The total installed, operating system-accessible memory (RAM), measured
       in GiB.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """


# ============================================


class LinksField(base.CompositeField):

    computer_system = base.Field(
        "ComputerSystem", adapter=utils.get_members_identities
    )
    """"""

    processors = base.Field("Processors", adapter=utils.get_members_identities)
    """"""

    memory = base.Field("Memory", adapter=utils.get_members_identities)
    """"""

    ethernet_interfaces = base.Field(
        "EthernetInterfaces", adapter=utils.get_members_identities
    )
    """"""

    local_drives = base.Field(
        "LocalDrives", adapter=utils.get_members_identities
    )
    """"""

    remote_drives = base.Field(
        "RemoteDrives", adapter=utils.get_members_identities
    )
    """"""

    managed_by = base.Field("ManagedBy", adapter=utils.get_members_identities)
    """"""


class ComposedNode(rsd_lib_base.ResourceBase):
    """ComposedNode resource class

       This schema defines a node and its respective properties.
    """

    links = LinksField("Links")
    """Contains links to other resources that are related to this resource."""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    composed_node_state = base.Field("ComposedNodeState")

    asset_tag = base.Field("AssetTag")
    """The user definable tag that can be used to track this computer system
       for inventory or other client purposes
    """

    uuid = base.Field("UUID")
    """The universal unique identifier (UUID) for this system"""

    power_state = base.Field("PowerState")
    """This is the current power state of the system"""

    boot = computer_system.BootField("Boot")
    """Information about the boot settings for this system"""

    processors = computer_system.ProcessorSummaryField("Processors")
    """This object describes the central processors of the system in general
       detail.
    """

    memory = computer_system.MemorySummaryField("Memory")
    """This object describes the central memory of the system in general
       detail.
    """


# TODO(linyang): Add Action Field


class ComposedNodeCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return ComposedNode
