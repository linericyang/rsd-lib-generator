from sushy.resources import base


from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import rack_location
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module

class RackLocationField(base.CompositeField):


    rack_units = base.Field("RackUnits")


    x_location = base.Field("XLocation", adapter=rsd_lib_utils.num_or_none)


    u_location = base.Field("ULocation", adapter=rsd_lib_utils.num_or_none)


    u_height = base.Field("UHeight", adapter=rsd_lib_utils.num_or_none)




# ============================================


class LinksField(base.CompositeField):




class PowerSupplyCollectionField(rsd_lib_base.ReferenceableMemberField):


    name = base.Field("Name")


    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    rack_location = rack_location.RackLocationField("RackLocation")


    serial_number = base.Field("SerialNumber")


    manufacturer = base.Field("Manufacturer")


    model_number = base.Field("ModelNumber")


    part_number = base.Field("PartNumber")


    firmware_revision = base.Field("FirmwareRevision")


    power_capacity_watts = base.Field("PowerCapacityWatts", adapter=rsd_lib_utils.num_or_none)


    last_power_output_watts = base.Field("LastPowerOutputWatts", adapter=rsd_lib_utils.num_or_none)



class PowerZone(rsd_lib_base.ResourceBase):


    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    rack_location = rack_location.RackLocationField("RackLocation")


    max_ps_us_supported = base.Field("MaxPSUsSupported", adapter=rsd_lib_utils.num_or_none)


    presence = base.Field("Presence")


    number_of_ps_us_present = base.Field("NumberOfPSUsPresent", adapter=rsd_lib_utils.num_or_none)


    power_consumed_watts = base.Field("PowerConsumedWatts", adapter=rsd_lib_utils.num_or_none)


    power_output_watts = base.Field("PowerOutputWatts", adapter=rsd_lib_utils.num_or_none)


    power_capacity_watts = base.Field("PowerCapacityWatts", adapter=rsd_lib_utils.num_or_none)


    power_supplies = PowerSupplyCollectionField("PowerSupplies")


    links = LinksField("Links")



# TODO(linyang): Add Action Field

class PowerZoneCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return PowerZone
