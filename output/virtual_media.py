from sushy.resources import base


from rsd_lib import base as rsd_lib_base


class VirtualMedia(rsd_lib_base.ResourceBase):
    """VirtualMedia resource class

       This resource allows monitoring and control of an instance of virtual
       media (e.g. a remote CD, DVD, or USB device) functionality provided by
       a Manager for a system or device.
    """

    image_name = base.Field("ImageName")
    """The current image name"""

    image = base.Field("Image")
    """A URI providing the location of the selected image"""

    media_types = base.Field("MediaTypes")
    """This is the media types supported as virtual media."""

    connected_via = base.Field("ConnectedVia")
    """Current virtual media connection methods"""

    inserted = base.Field("Inserted", adapter=bool)
    """Indicates if virtual media is inserted in the virtual device."""

    write_protected = base.Field("WriteProtected", adapter=bool)
    """Indicates the media is write protected."""


class VirtualMediaCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return VirtualMedia
