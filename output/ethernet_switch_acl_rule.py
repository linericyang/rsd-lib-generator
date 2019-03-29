from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base
# from  import forward_mirror_interface
# from  import mirror_port_region


from rsd_lib import utils as rsd_lib_utils




class MACConditionTypeField(base.CompositeField):


    mac_address = base.Field("MACAddress")


    mask = base.Field("Mask")



class LinksField(base.CompositeField):



class PortConditionTypeField(base.CompositeField):


    port = base.Field("Port", adapter=rsd_lib_utils.num_or_none)


    mask = base.Field("Mask", adapter=rsd_lib_utils.num_or_none)



class VlanIdConditionTypeField(base.CompositeField):


    id = base.Field("Id", adapter=rsd_lib_utils.num_or_none)


    mask = base.Field("Mask", adapter=rsd_lib_utils.num_or_none)



class IPConditionTypeField(base.CompositeField):


    i_pv4_address = base.Field("IPv4Address")


    mask = base.Field("Mask")



class ConditionTypeField(base.CompositeField):


    ip_source = IPConditionTypeField("IPSource")


    ip_destination = IPConditionTypeField("IPDestination")


    mac_source = MACConditionTypeField("MACSource")


    mac_destination = MACConditionTypeField("MACDestination")


    vlan_id = VlanIdConditionTypeField("VLANId")


    l4_source_port = PortConditionTypeField("L4SourcePort")


    l4_destination_port = PortConditionTypeField("L4DestinationPort")


    l4_protocol = base.Field("L4Protocol", adapter=rsd_lib_utils.num_or_none)
    """IP layer 4 protocol number"""



class EthernetSwitchACLRule(rsd_lib_base.ResourceBase):
    """EthernetSwitchACLRule resource class

       A Ethernet Switch ACL Rule represents Access Control List rule for
       switch.
    """


    rule_id = base.Field("RuleId", adapter=rsd_lib_utils.num_or_none)
    """This is ACL rule ID which determine rule priority."""

    action = base.Field("Action")
    """Action that will be executed when rule condition will be met.s"""

    mirror_type = base.Field("MirrorType")
    """Type of mirroring that should be use for Mirror action."""

    condition = ConditionTypeField("Condition")
    """Property contain set of conditions that should be met to trigger Rule
       action.
    """

    links = LinksField("Links")
    """Contains links to other resources that are related to this resource."""



    @property
    @utils.cache_it
    def forward_mirror_interface(self):
        """Property to provide reference to `EthernetSwitchPort` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return ethernet_switch_port.EthernetSwitchPort(
            self._conn,
            utils.get_sub_resource_path_by(self, "ForwardMirrorInterface"),
            redfish_version=self.redfish_version
        )



    @property
    @utils.cache_it
    def mirror_port_region(self):
        """Property to provide a list of `EthernetSwitchPort` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return [
            ethernet_switch_port.EthernetSwitchPort(
                self._conn,
                path,
                redfish_version=self.redfish_version)
            for path in rsd_lib_utils.get_sub_resource_path_list_by(self, "MirrorPortRegion")
        ]



class EthernetSwitchACLRuleCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return EthernetSwitchACLRule
