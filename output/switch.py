from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# from  import ports
# from  import log_services

# ============= import fields from other modules
# from  import redundancy
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class RedundancyCollectionField(rsd_lib_base.ReferenceableMemberField):
    """Redundancy field

       This is the common redundancy definition and structure used in other
       Redfish schemas.
    """


# ============================================


class LinksField(base.CompositeField):

    chassis = base.Field(
        "Chassis", adapter=rsd_lib_utils.get_resource_identity
    )
    """A reference to the chassis which contains this switch."""

    managed_by = base.Field("ManagedBy", adapter=utils.get_members_identities)
    """An array of references to the managers that manage this switch."""


class Switch(rsd_lib_base.ResourceBase):
    """Switch resource class

       Switch contains properties describing a simple fabric switch.
    """

    switch_type = base.Field("SwitchType")
    """The protocol being sent over this switch."""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    manufacturer = base.Field("Manufacturer")
    """This is the manufacturer of this switch."""

    model = base.Field("Model")
    """The product model number of this switch."""

    sku = base.Field("SKU")
    """This is the SKU for this switch."""

    serial_number = base.Field("SerialNumber")
    """The serial number for this switch."""

    part_number = base.Field("PartNumber")
    """The part number for this switch."""

    asset_tag = base.Field("AssetTag")
    """The user assigned asset tag for this switch."""

    domain_id = base.Field("DomainID", adapter=rsd_lib_utils.num_or_none)
    """The Domain ID for this switch."""

    is_managed = base.Field("IsManaged", adapter=bool)
    """This indicates whether the switch is in a managed or unmanaged state."""

    total_switch_width = base.Field(
        "TotalSwitchWidth", adapter=rsd_lib_utils.num_or_none
    )
    """The total number of lanes, phys, or other physical transport links that
       this switch contains.
    """

    indicator_led = base.Field("IndicatorLED")
    """The state of the indicator LED, used to identify the switch."""

    power_state = base.Field("PowerState")
    """This is the current power state of the switch."""

    links = LinksField("Links")
    """Contains references to other resources that are related to this
       resource.
    """

    redundancy = redundancy.RedundancyCollectionField("Redundancy")
    """Redundancy information for the switches"""

    # TODO(linyang): Add Action Field

    @property
    @utils.cache_it
    def ports(self):
        """Property to provide reference to `PortCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return port.PortCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Ports"),
            redfish_version=self.redfish_version,
        )

    @property
    @utils.cache_it
    def log_services(self):
        """Property to provide reference to `LogServiceCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return log_service.LogServiceCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "LogServices"),
            redfish_version=self.redfish_version,
        )


class SwitchCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return Switch
