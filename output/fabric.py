
from sushy import utils

from rsd_lib import base as rsd_lib_base
# from  import zones
# from  import endpoints
# from  import switches


from rsd_lib import utils as rsd_lib_utils




class LinksField(base.CompositeField):




class Fabric(rsd_lib_base.ResourceBase):
    """Fabric resource class

       Fabric contains properties describing a simple fabric consisting of one
       or more switches, zero or more endpoints, and zero or more zones.
    """


    fabric_type = base.Field("FabricType")
    """The protocol being sent over this fabric."""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    max_zones = base.Field("MaxZones", adapter=rsd_lib_utils.num_or_none)
    """The value of this property shall contain the maximum number of zones
       the switch can currently configure.
    """

    links = LinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """


# TODO(linyang): Add Action Field

    @property
    @utils.cache_it
    def zones(self):
        """Property to provide reference to `ZoneCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return zone.ZoneCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Zones"),
            redfish_version=self.redfish_version
        )



    @property
    @utils.cache_it
    def endpoints(self):
        """Property to provide reference to `EndpointCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return endpoint.EndpointCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Endpoints"),
            redfish_version=self.redfish_version
        )



    @property
    @utils.cache_it
    def switches(self):
        """Property to provide reference to `SwitchCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return switch.SwitchCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Switches"),
            redfish_version=self.redfish_version
        )



class FabricCollection(rsd_lib_base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return Fabric
