from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import resource
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class IdentifierCollectionField(rsd_lib_base.ReferenceableMemberField):

    durable_name = base.Field("DurableName")
    """This indicates the world wide, persistent name of the resource."""

    durable_name_format = base.Field("DurableNameFormat")
    """This represents the format of the DurableName property."""


# ============================================


class LinksField(base.CompositeField):

    drives = base.Field("Drives", adapter=utils.get_members_identities)
    """An array of references to the drives which contain this volume. This
       will reference Drives that either wholly or only partly contain this
       volume.
    """


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


class Volume(rsd_lib_base.ResourceBase):
    """Volume resource class

       Volume contains properties used to describe a volume, virtual disk,
       LUN, or other logical storage entity for any system.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    capacity_bytes = base.Field(
        "CapacityBytes", adapter=rsd_lib_utils.num_or_none
    )
    """The size in bytes of this Volume"""

    volume_type = base.Field("VolumeType")
    """The type of this volume"""

    encrypted = base.Field("Encrypted", adapter=bool)
    """Is this Volume encrypted"""

    encryption_types = base.Field("EncryptionTypes")
    """The types of encryption used by this Volume"""

    identifiers = resource.IdentifierCollectionField("Identifiers")
    """The Durable names for the volume"""

    block_size_bytes = base.Field(
        "BlockSizeBytes", adapter=rsd_lib_utils.num_or_none
    )
    """The size of the smallest addressible unit (Block) of this volume in
       bytes
    """

    operations = OperationsCollectionField("Operations")
    """The operations currently running on the Volume"""

    optimum_io_size_bytes = base.Field(
        "OptimumIOSizeBytes", adapter=rsd_lib_utils.num_or_none
    )
    """The size in bytes of this Volume's optimum IO size."""

    links = LinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """


# TODO(linyang): Add Action Field


class VolumeCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return Volume
