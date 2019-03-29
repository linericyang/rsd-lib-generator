from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base


from rsd_lib import utils as rsd_lib_utils


class LinksField(base.CompositeField):

    used_by = base.Field("UsedBy", adapter=utils.get_members_identities)


class PhysicalDrive(rsd_lib_base.ResourceBase):

    interface = base.Field("Interface")
    """Controller interface"""

    capacity_gi_b = base.Field(
        "CapacityGiB", adapter=rsd_lib_utils.num_or_none
    )
    """Drive capacity in GibiBytes."""

    type = base.Field("Type")
    """Type of drive"""

    rpm = base.Field("RPM", adapter=rsd_lib_utils.num_or_none)
    """For traditional drive, rotation per minute."""

    manufacturer = base.Field("Manufacturer")
    """Drive manufacturer name."""

    model = base.Field("Model")
    """Drive model"""

    serial_number = base.Field("SerialNumber")
    """Drive serial number"""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    links = LinksField("Links")


class PhysicalDriveCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return PhysicalDrive
