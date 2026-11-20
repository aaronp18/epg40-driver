from enum import IntFlag, IntEnum

"""
Based on JODELL EPG Series Instruction Manual, Version A.1.

Applies to the EPG series, including EPG40-050.

Register addresses are Modbus PDU addresses (zero-based as documented).
Registers are 16-bit. Byte positions are identified explicily.

Written with help from ChatGPT.

"""


class EPG40Register(IntEnum):

    # --------------------------------------------------------
    # Control registers (0x03E8 - 0x03FE)
    # --------------------------------------------------------

    CONTROL = 0x03E8
    POSITION = 0x03E9
    SPEED_FORCE = 0x03EA

    # Eight preset parameter groups
    PRESET_1_POSITION_SPEED = 0x03EB
    PRESET_1_FORCE = 0x03EC

    PRESET_2_POSITION_SPEED = 0x03ED
    PRESET_2_FORCE = 0x03EE

    PRESET_3_POSITION_SPEED = 0x03EF
    PRESET_3_FORCE = 0x03F0

    PRESET_4_POSITION_SPEED = 0x03F1
    PRESET_4_FORCE = 0x03F2

    PRESET_5_POSITION_SPEED = 0x03F3
    PRESET_5_FORCE = 0x03F4

    PRESET_6_POSITION_SPEED = 0x03F5
    PRESET_6_FORCE = 0x03F6

    PRESET_7_POSITION_SPEED = 0x03F7
    PRESET_7_FORCE = 0x03F8

    PRESET_8_POSITION_SPEED = 0x03F9
    PRESET_8_FORCE = 0x03FA

    ENCODER_ZERO = 0x03FB
    BRAKE_OVERRIDE = 0x03FC
    CONTROL_MODE_SWITCH = 0x03FD
    IO_MODE_SWITCH = 0x03FE

    # --------------------------------------------------------
    # Feedback registers (0x07D0 - 0x07D3)
    # --------------------------------------------------------

    GRIPPER_STATUS = 0x07D0
    FAULT_POSITION = 0x07D1
    SPEED_FORCE_STATUS = 0x07D2
    VOLTAGE_TEMPERATURE = 0x07D3

    # --------------------------------------------------------
    # Device configuration registers
    # --------------------------------------------------------

    FIRMWARE_VERSION = 0x138C
    DEVICE_ID = 0x138D
    BAUD_RATE = 0x138E

    DROP_THRESHOLD = 0x1399
    ENABLE_MODE = 0x139E
    BRAKE_MODE = 0x13A0
    BRAKE_FUNCTION = 0x13A4


class ControlBits(IntFlag):
    RACT = 1 << 0  # Activate gripper
    RMOD = 1 << 1  # Control mode
    RESERVED_2 = 1 << 2  # Reserved
    RGTO = 1 << 3  # Go to requested position
    RATR = 1 << 4  # Automatic release
    RARD = 1 << 5  # Release direction
    RESERVED_6 = 1 << 6
    RESERVED_7 = 1 << 7

    # Test individuual bits with `register & ControlBits.RACT`


class PresetCommand(IntEnum):
    """Commands in the HIGH byte of register 0x03E8.

    Used when RMODE = 1.
    """

    RESERVED_0 = 0x00

    HALF_SPEED_FORCE_OPEN = 0x01
    HALF_SPEED_FORCE_CLOSE = 0x02

    FULL_SPEED_FORCE_OPEN = 0x03
    FULL_SPEED_FORCE_CLOSE = 0x04

    LOW_SPEED_FORCE_OPEN = 0x05
    LOW_SPEED_FORCE_CLOSE = 0x06

    RESERVED_7 = 0x07

    PRESET_1 = 0x08
    PRESET_2 = 0x09
    PRESET_3 = 0x0A
    PRESET_4 = 0x0B
    PRESET_5 = 0x0C
    PRESET_6 = 0x0D
    PRESET_7 = 0x0E
    PRESET_8 = 0x0F


class InspectionDirection(IntEnum):
    """RARD bit direction."""

    CLOSE = 0
    OPEN = 1


class ControlMode(IntEnum):
    PARAMETER = 0
    PRESET = 1


class ByteField(IntFlag):
    """Masks for extracting high and low bytes."""

    LOW_BYTE = 0x00FF
    HIGH_BYTE = 0xFF00


POSITION_MIN = 0x00
POSITION_MAX = 0xFF

SPEED_MIN = 0x00
SPEED_MAX = 0xFF

FORCE_MIN = 0x00
FORCE_MAX = 0xFF


# ============================================================
# GRIPPER STATUS: 0x07D0
# ============================================================


class StatusBits(IntFlag):
    """Status fields in the LOW byte of register 0x07D0."""

    GACT = 1 << 0  # Gripper enabled
    GDROPSTA = 1 << 1  # Object-drop detection
    GMODE = 1 << 2  # Current control mode
    GGTO = 1 << 3  # Movement active

    # Activation / movement status occupies bits 4-5
    GSTA_MASK = 0b00110000

    # Object detection occupies bits 6-7
    GOBJ_MASK = 0b11000000


class ActivationStatus(IntEnum):
    RESET_OR_INSPECTION = 0
    ACTIVATING = 1
    RESERVED = 2
    ACTIVATION_COMPLETE = 3


class ObjectStatus(IntEnum):
    """Object detection feedback (bits 6-7)."""

    MOVING_TO_POSITION = 0
    INTERNAL_GRIP_DETECTED = 1
    EXTERNAL_GRIP_DETECTED = 2
    POSITION_REACHED_NO_OBJECT = 3


# ============================================================
# FAULT REGISTER: 0x07D1 LOW BYTE
# ============================================================


class FaultBits(IntFlag):
    """Fault flags in the LOW byte of register 0x07D1."""

    NOT_ACTIVATED = 1 << 0
    INVALID_COMMAND = 1 << 1
    COMMUNICATION_LOST = 1 << 2
    OVERCURRENT = 1 << 3
    VOLTAGE_ABNORMAL = 1 << 4
    ACTIVATION_ERROR = 1 << 5
    OVER_TEMPERATURE = 1 << 6
    INTERNAL_DEVICE_ERROR = 1 << 7


# ============================================================
# FEEDBACK BYTE FIELDS
# ============================================================

# Register 0x07D1
FAULT_MASK = 0x00FF
ACTUAL_POSITION_MASK = 0xFF00

# Register 0x07D2
ACTUAL_SPEED_MASK = 0x00FF
ACTUAL_CURRENT_MASK = 0xFF00

# Register 0x07D3
BUS_VOLTAGE_MASK = 0x00FF
AMBIENT_TEMPERATURE_MASK = 0xFF00


class SpecialRegisterValue(IntEnum):
    NORMAL = 0x00
    ENABLE = 0x01


class EncoderCommand(IntEnum):
    NORMAL = 0x00
    ZERO_ENCODER = 0x01


class BrakeOverrideCommand(IntEnum):
    NORMAL = 0x00
    FORCE_OPEN_BRAKE = 0x01


class ControlInterface(IntEnum):
    MODBUS = 0x00
    IO = 0x55


class BaudRate(IntEnum):
    """Values for register 0x138E."""

    BAUD_115200 = 0
    BAUD_57600 = 1
    BAUD_38400 = 2
    BAUD_19200 = 3
    BAUD_9600 = 4
    BAUD_4800 = 5


class EnableMode(IntEnum):
    SEARCH_STROKE = 0
    OPEN_ONLY = 1
    CLOSE_ONLY = 2


class BrakeMode(IntEnum):
    MOTION_ACTIVE = 0
    POWER_OFF_HOLD = 1


class BrakeFunction(IntEnum):
    DISABLED = 0
    ENABLED = 1


# ============================================================
# PRESET PARAMETER REGISTERS
# ============================================================

# Each preset contains:
# - Position: low byte of first register
# - Speed: high byte of first register
# - Force: low byte of second register

PRESET_REGISTERS = {
    1: (EPG40Register.PRESET_1_POSITION_SPEED, EPG40Register.PRESET_1_FORCE),
    2: (EPG40Register.PRESET_2_POSITION_SPEED, EPG40Register.PRESET_2_FORCE),
    3: (EPG40Register.PRESET_3_POSITION_SPEED, EPG40Register.PRESET_3_FORCE),
    4: (EPG40Register.PRESET_4_POSITION_SPEED, EPG40Register.PRESET_4_FORCE),
    5: (EPG40Register.PRESET_5_POSITION_SPEED, EPG40Register.PRESET_5_FORCE),
    6: (EPG40Register.PRESET_6_POSITION_SPEED, EPG40Register.PRESET_6_FORCE),
    7: (EPG40Register.PRESET_7_POSITION_SPEED, EPG40Register.PRESET_7_FORCE),
    8: (EPG40Register.PRESET_8_POSITION_SPEED, EPG40Register.PRESET_8_FORCE),
}


# ============================================================
# REGISTER PACKING / EXTRACTION HELPERS
# ============================================================


def pack_control(
    bits: ControlBits,
    command: PresetCommand = PresetCommand.RESERVED_0,
) -> int:
    """Pack control bits and preset command into 0x03E8."""

    return (int(command) << 8) | int(bits)


def pack_position(position: int) -> int:
    """Pack position into the high byte of 0x03E9."""

    _validate_byte(position, "position")
    return position << 8


def pack_speed_force(speed: int, force: int) -> int:
    """Pack speed into low byte and force into high byte."""

    _validate_byte(speed, "speed")
    _validate_byte(force, "force")

    return (force << 8) | speed


def unpack_high_byte(register_value: int) -> int:
    return (register_value >> 8) & 0xFF


def unpack_low_byte(register_value: int) -> int:
    return register_value & 0xFF


def _validate_byte(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")

    if not 0 <= value <= 0xFF:
        raise ValueError(f"{name} must be between 0 and 255")
