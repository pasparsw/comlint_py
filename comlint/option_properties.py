from dataclasses import dataclass
from comlint.types import OptionValues, OptionValue


@dataclass
class OptionProperties:
    description: str
    allowed_values: OptionValues
    default_value: OptionValue
