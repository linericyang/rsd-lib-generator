from sushy.resources import base


from rsd_lib import base as rsd_lib_base


class SerialInterface(rsd_lib_base.ResourceBase):
    """SerialInterface resource class

       This schema defines an asynchronous serial interface resource.
    """

    interface_enabled = base.Field("InterfaceEnabled", adapter=bool)
    """This indicates whether this interface is enabled."""

    signal_type = base.Field("SignalType")
    """The type of signal used for the communication connection - RS232 or
       RS485.
    """

    bit_rate = base.Field("BitRate")
    """The receive and transmit rate of data flow, typically in
       bits-per-second (bps), over the serial connection.
    """

    parity = base.Field("Parity")
    """The type of parity used by the sender and receiver in order to detect
       errors over the serial connection.
    """

    data_bits = base.Field("DataBits")
    """The number of data bits that will follow the start bit over the serial
       connection.
    """

    stop_bits = base.Field("StopBits")
    """The period of time before the next start bit is transmitted."""

    flow_control = base.Field("FlowControl")
    """The type of flow control, if any, that will be imposed on the serial
       connection.
    """

    connector_type = base.Field("ConnectorType")
    """The type of connector used for this interface."""

    pin_out = base.Field("PinOut")
    """The physical pin configuration needed for a serial connector."""


class SerialInterfaceCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return SerialInterface
