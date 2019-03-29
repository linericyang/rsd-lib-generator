from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# from  import ports
# from  import ac_ls


from rsd_lib import utils as rsd_lib_utils


class LinksField(base.CompositeField):

    chassis = base.Field(
        "Chassis", adapter=rsd_lib_utils.get_resource_identity
    )

    managed_by = base.Field("ManagedBy", adapter=utils.get_members_identities)


class EthernetSwitch(rsd_lib_base.ResourceBase):

    switch_id = base.Field("SwitchId")
    """Unique switch Id (within drawer) used to identify in switch hierarchy
       discovery.
    """

    manufacturer = base.Field("Manufacturer")
    """Switch manufacturer name"""

    model = base.Field("Model")
    """Switch model"""

    manufacturing_date = base.Field("ManufacturingDate")
    """Manufacturing date"""

    serial_number = base.Field("SerialNumber")
    """Switch serial numberSS"""

    part_number = base.Field("PartNumber")
    """Switch part number"""

    firmware_name = base.Field("FirmwareName")
    """Switch firmware name"""

    firmware_version = base.Field("FirmwareVersion")
    """Switch firmware version"""

    role = base.Field("Role")
    """"""

    max_acl_number = base.Field(
        "MaxACLNumber", adapter=rsd_lib_utils.num_or_none
    )
    """Role of switch"""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    links = LinksField("Links")

    @property
    @utils.cache_it
    def ports(self):
        """Property to provide reference to `EthernetSwitchPortCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return ethernet_switch_port.EthernetSwitchPortCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Ports"),
            redfish_version=self.redfish_version,
        )

    @property
    @utils.cache_it
    def ac_ls(self):
        """Property to provide reference to `EthernetSwitchACLCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return ethernet_switch_acl.EthernetSwitchACLCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "ACLs"),
            redfish_version=self.redfish_version,
        )


class EthernetSwitchCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return EthernetSwitch
