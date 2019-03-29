
from sushy import utils

from rsd_lib import base as rsd_lib_base
# from  import network_device_functions







class LinksField(base.CompositeField):




class NetworkInterface(rsd_lib_base.ResourceBase):
    """NetworkInterface resource class

       A NetworkInterface contains references linking  NetworkDeviceFunction
       resources and represents the functionality available to the containing
       system.
    """


    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    links = LinksField("Links")
    """Links."""



    @property
    @utils.cache_it
    def network_device_functions(self):
        """Property to provide reference to `NetworkDeviceFunctionCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return network_device_function.NetworkDeviceFunctionCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "NetworkDeviceFunctions"),
            redfish_version=self.redfish_version
        )



class NetworkInterfaceCollection(rsd_lib_base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return NetworkInterface
