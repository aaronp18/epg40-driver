from epg40_driver.transport import ITransport

import logging


class EPG40Gripper:

    _connected = False
    openPosition = 0
    closePosition = 0

    def __init__(
        self,
        transport: ITransport,
        name: str = "EPG40",
        openPosition: int = 0,
        closePosition: int = 0,
        force: int = 0,
        speed: int = 0,
    ):
        self.transport = transport
        self.name = name
        self.openPosition = openPosition
        self.closePosition = closePosition
        self.force = force
        self.speed = speed

        # Add prefix to all log messages from this module
        class CustomAdapter(logging.LoggerAdapter):
            _name: str

            def __init__(self, logger, name):
                super().__init__(logger, {})
                self._name = name

            def process(self, msg, kwargs):
                return f"[{self._name}] {msg}", kwargs

        self.logger = CustomAdapter(logging.getLogger(__name__), name)

        pass

    def begin(self):
        """Starts the connection to the gripper"""
        try:
            self.logger.info("Connecting to gripper...")
            result = self.transport.connect()
            self.logger.info("Gripper connected.")
            # TODO gripper activate
            self.activate()

            self._connected = result
            return True
        except Exception as e:
            self.logger.error("Error connecting to gripper: " + str(e))
            self._connected = False
        return False

    def end(self):
        try:
            self.transport.close()
        except Exception as e:
            self.logger.error("Error closing gripper connection: " + str(e))

    def activate(self):
        pass

    def isConnected(self):
        # TODO active connection check
        return self._connected

    def getStatus(self):
        """Gets the formatted status of the gripper"""
        pass

    def closeGripper(self):
        """Closes the gripper fully"""
        pass

    def openGripper(self):
        """Opens the gripper fully"""
        pass

    def setSpeed(self, speed: int):
        """Sets the speed of the gripper"""
        pass

    def setPosition(self, position: int):
        """Sets the position of the gripper"""
        pass

    def setForce(self, force: int):
        """Sets the force of the gripper"""
        pass

    def setSpeedForce(self, speed: int, force: int):
        """Sets the speed and force of the gripper"""
        self.setSpeed(speed)
        self.setForce(force)
        pass

    def setOpenPosition(self, position: int):
        """Sets the open position of the gripper"""
        pass

    def setClosePosition(self, position: int):
        """Sets the close position of the gripper"""
        pass
