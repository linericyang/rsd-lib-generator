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




class TemperatureSensorCollectionField(rsd_lib_base.ReferenceableMemberField):


    name = base.Field("Name")


    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    reading_celsius = base.Field("ReadingCelsius", adapter=rsd_lib_utils.num_or_none)


    physical_context = base.Field("PhysicalContext")



class FanCollectionField(rsd_lib_base.ReferenceableMemberField):


    name = base.Field("Name")


    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    reading_rpm = base.Field("ReadingRPM", adapter=rsd_lib_utils.num_or_none)


    rack_location = rack_location.RackLocationField("RackLocation")



class ThermalZone(rsd_lib_base.ResourceBase):


    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    rack_location = rack_location.RackLocationField("RackLocation")


    presence = base.Field("Presence")


    desired_speed_pwm = base.Field("DesiredSpeedPWM", adapter=rsd_lib_utils.num_or_none)


    desired_speed_rpm = base.Field("DesiredSpeedRPM", adapter=rsd_lib_utils.num_or_none)


    max_fans_supported = base.Field("MaxFansSupported", adapter=rsd_lib_utils.num_or_none)


    number_of_fans_present = base.Field("NumberOfFansPresent", adapter=rsd_lib_utils.num_or_none)


    volumetric_airflow = base.Field("VolumetricAirflow", adapter=rsd_lib_utils.num_or_none)


    temperatures = TemperatureSensorCollectionField("Temperatures")


    fans = FanCollectionField("Fans")



    links = LinksField("Links")


# TODO(linyang): Add Action Field

class ThermalZoneCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return ThermalZone
