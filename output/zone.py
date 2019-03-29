from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base


class LinksField(base.CompositeField):

    endpoints = base.Field("Endpoints", adapter=utils.get_members_identities)
    """An array of references to the endpoints that are contained in this zone.
    """

    involved_switches = base.Field(
        "InvolvedSwitches", adapter=utils.get_members_identities
    )
    """An array of references to the switchs that are utilized in this zone."""


class Zone(rsd_lib_base.ResourceBase):
    """Zone resource class

       Switch contains properties describing a simple fabric zone.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    links = LinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """


class ZoneCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return Zone
