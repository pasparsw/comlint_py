from abc import abstractmethod
from comlint.parsed_command import ParsedCommand


class CommandHandlerInterface:
    @abstractmethod
    def run(self, command: ParsedCommand) -> None:
        pass
