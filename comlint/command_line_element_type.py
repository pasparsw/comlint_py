from enum import Enum


class CommandLineElementType(Enum):
    COMMAND = 0
    OPTION = 1
    FLAG = 2
    CUSTOM_VALUE = 3
