
from gnmi_api.gnmi_manager import gNMIManager
import grpc


class GNMIManagerV2(gNMIManager):
    def connect(self) -> None:
        """
        Connect to the gNMI device

        """
        try:
            if self.pem == '':
                self.channel: grpc.insecure_channel = grpc.insecure_channel(':'.join([self.host, self.port]),
                                                                            self.options)
            else:
                credentials: grpc.ssl_channel_credentials = grpc.ssl_channel_credentials(self._read_pem())
                self.channel: grpc.secure_channel = grpc.secure_channel(':'.join([self.host, self.port]), credentials,
                                                                        self.options)

            grpc.channel_ready_future(self.channel).result(timeout=10)
            self._connected = True
        except grpc.FutureTimeoutError:
            raise GNMIException(f'Unable to connect to "{self.host}:{self.port}"')

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class GNMIException(Exception):
    """ Exception for GNMI API Errors """
    pass
