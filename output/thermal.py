from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import redundancy
# =============

from rsd_lib import utils as rsd_lib_utils


# =========== Fields should be in other module


class RedundancyCollectionField(rsd_lib_base.ReferenceableMemberField):
    """Redundancy field

       This is the redundancy definition to be used in other resource schemas.
    """

    name = base.Field("Name")
    """The name of the resource or array element."""

    mode = base.Field("Mode")
    """This is the redundancy mode of the group."""

    max_num_supported = base.Field(
        "MaxNumSupported", adapter=rsd_lib_utils.num_or_none
    )
    """This is the maximum number of members allowable for this particular
       redundancy group.
    """

    min_num_needed = base.Field(
        "MinNumNeeded", adapter=rsd_lib_utils.num_or_none
    )
    """This is the minumum number of members needed for this group to be
       redundant.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    redundancy_set = base.Field(
        "RedundancySet", adapter=utils.get_members_identities
    )
    """Contains any ids that represent components of this redundancy set."""

    redundancy_enabled = base.Field("RedundancyEnabled", adapter=bool)
    """This indicates whether redundancy is enabled."""


# ============================================


class FanCollectionField(rsd_lib_base.ReferenceableMemberField):

    fan_name = base.Field("FanName")
    """Name of the fan"""

    physical_context = base.Field("PhysicalContext")
    """Describes the area or device associated with this fan."""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    reading = base.Field("Reading", adapter=rsd_lib_utils.num_or_none)
    """Current fan speed"""

    upper_threshold_non_critical = base.Field(
        "UpperThresholdNonCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Above normal range"""

    upper_threshold_critical = base.Field(
        "UpperThresholdCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Above normal range but not yet fatal"""

    upper_threshold_fatal = base.Field(
        "UpperThresholdFatal", adapter=rsd_lib_utils.num_or_none
    )
    """Above normal range and is fatal"""

    lower_threshold_non_critical = base.Field(
        "LowerThresholdNonCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Below normal range"""

    lower_threshold_critical = base.Field(
        "LowerThresholdCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Below normal range but not yet fatal"""

    lower_threshold_fatal = base.Field(
        "LowerThresholdFatal", adapter=rsd_lib_utils.num_or_none
    )
    """Below normal range and is fatal"""

    min_reading_range = base.Field(
        "MinReadingRange", adapter=rsd_lib_utils.num_or_none
    )
    """Minimum value for Reading"""

    max_reading_range = base.Field(
        "MaxReadingRange", adapter=rsd_lib_utils.num_or_none
    )
    """Maximum value for Reading"""

    related_item = base.Field(
        "RelatedItem", adapter=utils.get_members_identities
    )
    """The ID(s) of the resources serviced with this fan"""

    redundancy = redundancy.RedundancyCollectionField("Redundancy")
    """This structure is used to show redundancy for fans.  The Component ids
       will reference the members of the redundancy groups.
    """

    reading_units = base.Field("ReadingUnits")
    """Units in which the reading and thresholds are measured."""

    name = base.Field("Name")
    """Name of the fan"""


class TemperatureCollectionField(rsd_lib_base.ReferenceableMemberField):

    name = base.Field("Name")
    """Temperature sensor name."""

    sensor_number = base.Field(
        "SensorNumber", adapter=rsd_lib_utils.num_or_none
    )
    """A numerical identifier to represent the temperature sensor"""

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    reading_celsius = base.Field(
        "ReadingCelsius", adapter=rsd_lib_utils.num_or_none
    )
    """Temperature"""

    upper_threshold_non_critical = base.Field(
        "UpperThresholdNonCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Above normal range"""

    upper_threshold_critical = base.Field(
        "UpperThresholdCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Above normal range but not yet fatal."""

    upper_threshold_fatal = base.Field(
        "UpperThresholdFatal", adapter=rsd_lib_utils.num_or_none
    )
    """Above normal range and is fatal"""

    lower_threshold_non_critical = base.Field(
        "LowerThresholdNonCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Below normal range"""

    lower_threshold_critical = base.Field(
        "LowerThresholdCritical", adapter=rsd_lib_utils.num_or_none
    )
    """Below normal range but not yet fatal."""

    lower_threshold_fatal = base.Field(
        "LowerThresholdFatal", adapter=rsd_lib_utils.num_or_none
    )
    """Below normal range and is fatal"""

    min_reading_range_temp = base.Field(
        "MinReadingRangeTemp", adapter=rsd_lib_utils.num_or_none
    )
    """Minimum value for ReadingCelsius"""

    max_reading_range_temp = base.Field(
        "MaxReadingRangeTemp", adapter=rsd_lib_utils.num_or_none
    )
    """Maximum value for ReadingCelsius"""

    physical_context = base.Field("PhysicalContext")
    """Describes the area or device to which this temperature measurement
       applies.
    """

    related_item = base.Field(
        "RelatedItem", adapter=utils.get_members_identities
    )
    """Describes the areas or devices to which this temperature measurement
       applies.
    """


class Thermal(rsd_lib_base.ResourceBase):
    """Thermal resource class

       This is the schema definition for the Thermal properties.  It
       represents the properties for Temperature and Cooling.
    """

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    temperatures = TemperatureCollectionField("Temperatures")
    """This is the definition for temperature sensors."""

    fans = FanCollectionField("Fans")
    """This is the definition for fans."""

    redundancy = redundancy.RedundancyCollectionField("Redundancy")
    """This structure is used to show redundancy for fans.  The Component ids
       will reference the members of the redundancy groups.
    """
