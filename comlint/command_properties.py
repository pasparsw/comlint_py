from dataclasses import dataclass
from comlint.command_handler_interface import CommandHandlerInterface
from comlint.types import CommandValues, OptionNames, FlagNames


@dataclass
class CommandProperties:
    allowed_values: CommandValues
    allowed_options: OptionNames
    allowed_flags: FlagNames
    description: str
    num_of_required_values: int
    required_options: OptionNames
    command_handler: CommandHandlerInterface = None

    def requires_value(self) -> bool:
        return self.num_of_required_values > 0
