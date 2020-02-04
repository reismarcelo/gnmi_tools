
from gnmi_api.gnmi_manager import gNMIManager, GNMIException
import grpc


class GNMIManagerV2(gNMIManager):
    def __init__(self, *args, pem=None, encoding='JSON_IETF', **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.channel = None
        self.encoding = encoding
        if pem is not None:
            with open(pem, "rb") as fp:
                self.pem = fp.read()
        else:
            self.pem = None

    def connect(self) -> None:
        """Connect to the gNMI device
        """
        try:
            if self.pem is None:
                self.channel: grpc.insecure_channel = grpc.insecure_channel(':'.join([self.host, self.port]),
                                                                            self.options)
            else:
                credentials: grpc.ssl_channel_credentials = grpc.ssl_channel_credentials(self.pem)
                self.channel: grpc.secure_channel = grpc.secure_channel(':'.join([self.host, self.port]), credentials,
                                                                        self.options)

            grpc.channel_ready_future(self.channel).result(timeout=10)
            self._connected = True
        except grpc.FutureTimeoutError:
            raise GNMIException(f'Unable to connect to "{self.host}:{self.port}"')

    def get_config(self, *args, **kwargs):
        super().get_config(encoding=self.encoding, *args, **kwargs)
