from sushy.resources import base


from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import resource
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class OemField(base.CompositeField):
    """Oem field

       Oem extension object.
    """


# ============================================


class DeviceCollectionField(rsd_lib_base.ReferenceableMemberField):

    oem = resource.OemField("Oem")

    name = base.Field("Name")
    """The name of the resource or array element."""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    manufacturer = base.Field("Manufacturer")
    """The name of the manufacturer of this device"""

    model = base.Field("Model")
    """The product model number of this device"""

    capacity_bytes = base.Field(
        "CapacityBytes", adapter=rsd_lib_utils.num_or_none
    )
    """The size of the storage device."""


class SimpleStorage(rsd_lib_base.ResourceBase):
    """SimpleStorage resource class

       This is the schema definition for the Simple Storage resource.  It
       represents the properties of a storage controller and its
       directly-attached devices.
    """

    uefi_device_path = base.Field("UefiDevicePath")
    """The UEFI device path used to access this storage controller."""

    devices = DeviceCollectionField("Devices")
    """The storage devices associated with this resource"""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """


class SimpleStorageCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return SimpleStorage
