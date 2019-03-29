from sushy.resources import base


from rsd_lib import base as rsd_lib_base

# ============= import fields from other modules
# from  import resource
# =============


# =========== Fields should be in other module


class OemField(base.CompositeField):
    """Oem field

       Oem extension object.
    """


class ItemCollectionField(base.ListField):
    """Item field

       This is the base type for resources and referenceable members.
    """

    oem = resource.OemField("Oem")
    """This is the manufacturer/provider specific extension moniker used to
       divide the Oem object into sections.
    """


# ============================================


class HttpHeaderPropertyCollectionField(base.ListField):
    """HttpHeaderProperty field

       The value of the HTTP header is the property value.  The header name is
       the property name.
    """


class EventDestination(rsd_lib_base.ResourceBase):
    """EventDestination resource class

       An Event Destination desribes the target of an event subscription,
       including the types of events subscribed and context to provide to the
       target in the Event payload.
    """

    destination = base.Field("Destination")
    """The URI of the destination Event Service."""

    event_types = base.Field("EventTypes")
    """This property shall contain the types of events that shall be sent to
       the desination.
    """

    context = base.Field("Context")
    """A client-supplied string that is stored with the event destination
       subscription.
    """

    protocol = base.Field("Protocol")
    """The protocol type of the event connection."""

    http_headers = HttpHeaderPropertyCollectionField("HttpHeaders")
    """This is for setting HTTP headers, such as authorization information. 
       This object will be null on a GET.
    """

    message_ids = base.Field("MessageIds")
    """A list of MessageIds that the service will only send."""

    origin_resources = resource.ItemCollectionField("OriginResources")
    """A list of resources for which the service will only send related events.
    """


class EventDestinationCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return EventDestination
