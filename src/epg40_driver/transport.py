# Enables interoperabilityy between serial and tcp connections.

from abc import ABC, abstractmethod

from pymodbus.client import (
    ModbusSerialClient,
    ModbusTcpClient,
)


class ITransport(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self) -> bool:
        "Connect to the device"

    @abstractmethod
    def close(self) -> None:
        "Close the connection"

    @abstractmethod
    def writeRegister(self, register: int, value: int) -> None:
        "Write a value to a register"

    # TODO


class SerialTransport(ITransport):
    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        slave_id: int = 9,
    ):
        self.slave_id = slave_id
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=1,
        )

    def connect(self):
        return self.client.connect()

    def close(self):
        self.client.close()


class TCPTransport(ITransport):
    def __init__(
        self,
        host: str,
        port: int = 502,
        slave_id: int = 9,
    ):
        self.slave_id = slave_id
        self.client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=1,
        )

    def connect(self):
        return self.client.connect()

    def close(self):
        self.client.close()
