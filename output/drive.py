from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import resource
# from  import volume
# from  import storage
# from  import pc_ie_function
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class OemField(base.CompositeField):
    """Oem field

       Oem extension object.
    """


class StorageField(base.CompositeField):
    """Storage field

       Storage defines a storage subsystem and its respective properties.  A
       storage subsystem represents a set of storage controllers (physical or
       virtual) and the resources such as volumes that can be accessed from
       that subsystem.
    """


class PCIeFunctionField(base.CompositeField):
    """PCIeFunction field

       This is the schema definition for the PCIeFunction resource.  It
       represents the properties of a PCIeFunction attached to a System.
    """


class LocationCollectionField(rsd_lib_base.ReferenceableMemberField):

    info = base.Field("Info")
    """This indicates the location of the resource."""

    info_format = base.Field("InfoFormat")
    """This represents the format of the Info property."""

    oem = resource.OemField("Oem")


class OperationsCollectionField(rsd_lib_base.ReferenceableMemberField):

    operation_name = base.Field("OperationName")
    """The name of the operation."""

    percentage_complete = base.Field(
        "PercentageComplete", adapter=rsd_lib_utils.num_or_none
    )
    """The percentage of the operation that has been completed."""

    associated_task = base.Field(
        "AssociatedTask", adapter=rsd_lib_utils.get_resource_identity
    )
    """A reference to the task associated with the operation if any."""


class IdentifierCollectionField(rsd_lib_base.ReferenceableMemberField):

    durable_name = base.Field("DurableName")
    """This indicates the world wide, persistent name of the resource."""

    durable_name_format = base.Field("DurableNameFormat")
    """This represents the format of the DurableName property."""


# ============================================


class IntelRackScaleField(base.CompositeField):

    erase_on_detach = base.Field("EraseOnDetach", adapter=bool)
    """This indicates if drive should be erased when detached from PCI switch.
    """

    drive_erased = base.Field("DriveErased", adapter=bool)
    """This indicates whether drive was cleared after assignment to composed
       node.
    """

    firmware_version = base.Field("FirmwareVersion")
    """This indicates drive firmware version."""

    storage = storage.StorageField("Storage")
    """A reference to the storage controller where this drive is connected."""

    pc_ie_function = pc_ie_function.PCIeFunctionField("PCIeFunction")
    """A reference to the PCIe function that provides this drive functionality.
    """


class LinksField(base.CompositeField):

    volumes = base.Field("Volumes", adapter=utils.get_members_identities)
    """An array of references to the volumes contained in this drive. This
       will reference Volumes that are either wholly or only partly contained
       by this drive.
    """

    endpoints = base.Field("Endpoints", adapter=utils.get_members_identities)
    """An array of references to the endpoints that connect to this drive."""


class OemField(base.CompositeField):

    intel_rackscale = IntelRackScaleField("Intel_RackScale")
    """Intel Rack Scale Design specific properties."""


class Drive(rsd_lib_base.ResourceBase):
    """Drive resource class

       Drive contains properties describing a single physical disk drive for
       any system, along with links to associated Volumes.
    """

    status_indicator = base.Field("StatusIndicator")
    """The state of the status indicator, used to communicate status
       information about this drive.
    """

    indicator_led = base.Field("IndicatorLED")
    """The state of the indicator LED, used to identify the drive."""

    model = base.Field("Model")
    """This is the model number for the drive."""

    revision = base.Field("Revision")
    """The revision of this Drive"""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    capacity_bytes = base.Field(
        "CapacityBytes", adapter=rsd_lib_utils.num_or_none
    )
    """The size in bytes of this Drive"""

    failure_predicted = base.Field("FailurePredicted", adapter=bool)
    """Is this drive currently predicting a failure in the near future"""

    protocol = base.Field("Protocol")
    """The protocol this drive is using to communicate to the storage
       controller
    """

    media_type = base.Field("MediaType")
    """The type of media contained in this drive"""

    manufacturer = base.Field("Manufacturer")
    """This is the manufacturer of this drive."""

    sku = base.Field("SKU")
    """This is the SKU for this drive."""

    serial_number = base.Field("SerialNumber")
    """The serial number for this drive."""

    part_number = base.Field("PartNumber")
    """The part number for this drive."""

    asset_tag = base.Field("AssetTag")
    """The user assigned asset tag for this drive."""

    identifiers = resource.IdentifierCollectionField("Identifiers")
    """The Durable names for the drive"""

    location = resource.LocationCollectionField("Location")
    """The Location of the drive"""

    hotspare_type = base.Field("HotspareType")
    """The type of hotspare this drive is currently serving as"""

    encryption_ability = base.Field("EncryptionAbility")
    """The encryption abilities of this drive"""

    encryption_status = base.Field("EncryptionStatus")
    """The status of the encryption of this drive"""

    rotation_speed_rpm = base.Field(
        "RotationSpeedRPM", adapter=rsd_lib_utils.num_or_none
    )
    """The rotation speed of this Drive in Revolutions per Minute (RPM)"""

    block_size_bytes = base.Field(
        "BlockSizeBytes", adapter=rsd_lib_utils.num_or_none
    )
    """The size of the smallest addressible unit (Block) of this drive in bytes
    """

    capable_speed_gbs = base.Field(
        "CapableSpeedGbs", adapter=rsd_lib_utils.num_or_none
    )
    """The speed which this drive can communicate to a storage controller in
       ideal conditions in Gigabits per second
    """

    negotiated_speed_gbs = base.Field(
        "NegotiatedSpeedGbs", adapter=rsd_lib_utils.num_or_none
    )
    """The speed which this drive is currently communicating to the storage
       controller in Gigabits per second
    """

    predicted_media_life_left_percent = base.Field(
        "PredictedMediaLifeLeftPercent", adapter=rsd_lib_utils.num_or_none
    )
    """The percentage of reads and writes that are predicted to still be
       available for the media
    """

    links = LinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """

    operations = volume.OperationsCollectionField("Operations")
    """The operations currently running on the Drive."""

    oem = OemField("Oem")
    """Oem specific properties."""


# TODO(linyang): Add Action Field
