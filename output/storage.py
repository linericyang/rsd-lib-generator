from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# from  import drives
# from  import volumes

# ============= import fields from other modules
# from  import redundancy
# from  import resource
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class IdentifierCollectionField(rsd_lib_base.ReferenceableMemberField):

    durable_name = base.Field("DurableName")
    """This indicates the world wide, persistent name of the resource."""

    durable_name_format = base.Field("DurableNameFormat")
    """This represents the format of the DurableName property."""


class RedundancyCollectionField(rsd_lib_base.ReferenceableMemberField):
    """Redundancy field

       This is the common redundancy definition and structure used in other
       Redfish schemas.
    """


# ============================================


class StorageControllerLinksField(base.CompositeField):

    endpoints = base.Field("Endpoints", adapter=utils.get_members_identities)
    """An array of references to the endpoints that connect to this controller.
    """


class LinksField(base.CompositeField):

    enclosures = base.Field("Enclosures", adapter=utils.get_members_identities)
    """An array of references to the chassis to which this storage subsystem
       is attached
    """


class StorageControllerCollectionField(rsd_lib_base.ReferenceableMemberField):
    """StorageController field

       This schema defines a storage controller and its respective properties.
       A storage controller represents a storage device (physical or virtual)
       that produces Volumes.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    speed_gbps = base.Field("SpeedGbps", adapter=rsd_lib_utils.num_or_none)
    """The speed of the storage controller interface."""

    firmware_version = base.Field("FirmwareVersion")
    """The firmware version of this storage Controller"""

    manufacturer = base.Field("Manufacturer")
    """This is the manufacturer of this storage controller."""

    model = base.Field("Model")
    """This is the model number for the storage controller."""

    sku = base.Field("SKU")
    """This is the SKU for this storage controller."""

    serial_number = base.Field("SerialNumber")
    """The serial number for this storage controller."""

    part_number = base.Field("PartNumber")
    """The part number for this storage controller."""

    asset_tag = base.Field("AssetTag")
    """The user assigned asset tag for this storage controller."""

    supported_controller_protocols = base.Field("SupportedControllerProtocols")
    """This represents the protocols by which this storage controller can be
       communicated to.
    """

    supported_device_protocols = base.Field("SupportedDeviceProtocols")
    """This represents the protocols which the storage controller can use to
       communicate with attached devices.
    """

    identifiers = resource.IdentifierCollectionField("Identifiers")
    """The Durable names for the storage controller"""

    links = StorageControllerLinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """


class Storage(rsd_lib_base.ResourceBase):
    """Storage resource class

       This schema defines a storage subsystem and its respective properties. 
       A storage subsystem represents a set of storage controllers (physical
       or virtual) and the resources such as volumes that can be accessed from
       that subsystem.
    """

    links = LinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    storage_controllers = StorageControllerCollectionField(
        "StorageControllers"
    )
    """The set of storage controllers represented by this resource."""

    redundancy = redundancy.RedundancyCollectionField("Redundancy")
    """Redundancy information for the storage subsystem"""

    # TODO(linyang): Add Action Field

    @property
    @utils.cache_it
    def drives(self):
        """Property to provide a list of `Drive` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return [
            drive.Drive(self._conn, path, redfish_version=self.redfish_version)
            for path in rsd_lib_utils.get_sub_resource_path_list_by(
                self, "Drives"
            )
        ]

    @property
    @utils.cache_it
    def volumes(self):
        """Property to provide reference to `VolumeCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return volume.VolumeCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Volumes"),
            redfish_version=self.redfish_version,
        )


class StorageCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return Storage
