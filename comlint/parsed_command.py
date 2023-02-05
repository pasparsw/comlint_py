from dataclasses import dataclass
from comlint.types import CommandName, CommandValues, OptionsMap, FlagsMap, OptionName


@dataclass
class ParsedCommand:
    name: CommandName
    values: CommandValues
    options: OptionsMap
    flags: FlagsMap

    def is_option_used(self, option_name: OptionName) -> bool:
        return option_name in self.options.keys()
