from sushy.resources import base


from rsd_lib import base as rsd_lib_base







class MessagePropertyField(base.CompositeField):




class MessageRegistry(rsd_lib_base.ResourceBase):
    """MessageRegistry resource class

       This is the schema definition for all Message Registries.  It
       represents the properties for the registries themselves.  The MessageId
       is formed per the Redfish specification.  It consists of the
       RegistryPrefix concatenated with the version concatenated with the
       unique identifier for the message registry entry.
    """


    language = base.Field("Language")
    """This is the RFC 5646 compliant language code for the registry."""

    registry_prefix = base.Field("RegistryPrefix")
    """This is the single word prefix used to form a messageID structure."""

    registry_version = base.Field("RegistryVersion")
    """This is the message registry version which is used in the middle
       portion of a messageID.
    """

    owning_entity = base.Field("OwningEntity")
    """This is the organization or company that publishes this registry."""

    messages = MessagePropertyField("Messages")
    """The pattern property indicates that a free-form string is the unique
       identifier for the message within the registry.
    """



class MessageRegistryCollection(rsd_lib_base.ResourceCollectionBase):

    @property
    def _resource_type(self):
        return MessageRegistry
