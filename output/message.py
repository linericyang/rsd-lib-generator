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


# ============================================


class Message(rsd_lib_base.ResourceBase):

    message_id = base.Field("MessageId")
    """This is the key for this message which can be used to look up the
       message in a message registry.
    """

    message = base.Field("Message")
    """This is the human readable message, if provided."""

    related_properties = base.Field("RelatedProperties")
    """This is an array of properties described by the message."""

    message_args = base.Field("MessageArgs")
    """This array of message arguments are substituted for the arguments in
       the message when looked up in the message registry.
    """

    severity = base.Field("Severity")
    """This is the severity of the errors."""

    resolution = base.Field("Resolution")
    """Used to provide suggestions on how to resolve the situation that caused
       the error.
    """

    oem = resource.OemField("Oem")
    """Oem extension object."""
