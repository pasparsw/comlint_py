from abc import abstractmethod
from comlint.types import CommandValues, OptionsMap, FlagsMap


class CommandHandlerInterface:
    @abstractmethod
    def run(self, values: CommandValues, options: OptionsMap, flags: FlagsMap) -> None:
        pass
