from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base


from rsd_lib import utils as rsd_lib_utils


class LinksField(base.CompositeField):

    logical_drives = base.Field(
        "LogicalDrives", adapter=utils.get_members_identities
    )

    physical_drives = base.Field(
        "PhysicalDrives", adapter=utils.get_members_identities
    )

    master_drive = base.Field(
        "MasterDrive", adapter=rsd_lib_utils.get_resource_identity
    )

    used_by = base.Field("UsedBy", adapter=utils.get_members_identities)

    targets = base.Field("Targets", adapter=utils.get_members_identities)


class LogicalDrive(rsd_lib_base.ResourceBase):

    type = base.Field("Type")
    """Type of volume"""

    mode = base.Field("Mode")
    """Mode defines how the logical drive is built on top of underlying
       physical/logical drives. The value shall correspond to the logical
       drive type.
    """

    protected = base.Field("Protected", adapter=bool)
    """Write (modify) protection state."""

    capacity_gi_b = base.Field(
        "CapacityGiB", adapter=rsd_lib_utils.num_or_none
    )
    """Drive capacity in GibiBytes."""

    image = base.Field("Image")
    """Image name."""

    bootable = base.Field("Bootable", adapter=bool)
    """Specify if target is bootable."""

    snapshot = base.Field("Snapshot", adapter=bool)
    """Indicates if the logical drive should be created as a snapshot of the
       source master drive, or should be created as a full copy of an image
       from the source master drive.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    links = LinksField("Links")


class LogicalDriveCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return LogicalDrive
