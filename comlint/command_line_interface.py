from typing import List
import comlint.utils as utils
from comlint.command_handler_interface import CommandHandlerInterface
from comlint.command_line_element_type import CommandLineElementType
from comlint.command_properties import CommandProperties
from comlint.exceptions.forbidden_flag import ForbiddenFlag
from comlint.exceptions.forbidden_option import ForbiddenOption
from comlint.exceptions.forbidden_option_value import ForbiddenOptionValue
from comlint.exceptions.invalid_command_position import InvalidCommandPosition
from comlint.exceptions.missing_command_handler import MissingCommandHandler
from comlint.exceptions.missing_command_value import MissingCommandValue
from comlint.exceptions.missing_option_value import MissingOptionValue
from comlint.exceptions.missing_required_option import MissingRequiredOption
from comlint.exceptions.unsupported_command import UnsupportedCommand
from comlint.exceptions.unsupported_command_value import UnsupportedCommandValue
from comlint.exceptions.unsupported_flag import UnsupportedFlag
from comlint.exceptions.unsupported_option import UnsupportedOption
from comlint.flag_properties import FlagProperties
from comlint.interface_helper import Commands, Options, Flags, InterfaceHelper
from comlint.interface_validator import InterfaceValidator
from comlint.option_properties import OptionProperties
from comlint.parsed_command import ParsedCommand
from comlint.types import CommandValues, ANY, OptionNames, NONE, FlagNames, OptionName, OptionValues, OptionValue, \
    FlagName, CommandName, OptionsMap, FlagsMap, CommandValue

DEFAULT_OPTION_VALUE: OptionValue = ''


class CommandLineInterface:
    """
    Class allowing user to create their own custom command line interfaces which are designed around commands. There are
    3 types of interface building blocks which may be added by the user:
        - command - keyword specifying an action which should be executed. Command is always placed after executable
                    name and is a word without any particular prefix or sufix. Command may or may not take a value which
                    details its behavior. Scheme of usage of command without value:
                                          program_name [command_name]
                    Scheme of usage of command taking value:
                                          program_name [command_name] [command_value]
                    Example of usage of command without value, where "pull" is a command name:
                                          git pull
                    Example of usage of command taking value, where "add" is a command name and "/some/file.txt" is a
                    command value:
                                          git add /some/file.txt
        - option - keyword providing additional information for the command execution. It is always prefixed with a
                   single dash "-" and always takes a value. Scheme of usage of command with a single option:
                                          program_name [command_name] [option_name] [option_value]
                   Scheme of usage of command with multiple options:
                                          program_name [command_name] [option_name_1] [option_value_1] [option_name_2] [option_value_2]
                   Example of usage of command with an option, where "install" is a command name, "-r" is option name
                   and "requirements.txt" is option value:
                                          pip install -r requirements.txt
        - flag - keyword enabling or disabling some functionalities during command execution. It is always prefixed with
                 a double dash "--" and never takes any value. Scheme of usage of command with a single flag:
                                          program_name [command_name] [flag]
                 Example of usage of command with a single flag, where "pull" is a command name and "--rebase" is a flag:
                                          git pull --rebase
    """
    def __init__(self, argv: List[str], program_name: str = '', description: str = '', allow_no_arguments: bool = True):
        self.__argv: List[str] = argv
        self.__program_name: str = program_name if program_name else argv[0]
        self.__description: str = description
        self.__allow_no_arguments: bool = allow_no_arguments
        self.__interface_commands: Commands = {}
        self.__interface_options: Options = {}
        self.__interface_flags: Flags = {}

    def add_command(self, command_name: str, description: str, num_of_required_values: int = 0,
                    allowed_values: CommandValues = ANY, allowed_options: OptionNames = NONE,
                    allowed_flags: FlagNames = NONE, required_options: OptionNames = NONE) -> None:
        # TODO: make these separate exceptions
        if not InterfaceValidator.is_command_name_valid(command_name):
            print(f'Unable to add command {command_name} - command name invalid')
            return
        if command_name in self.__interface_commands.keys():
            print(f'Unable to add command {command_name} - command with the same name already added')
            return

        self.__interface_commands[command_name] = CommandProperties(allowed_values, allowed_options, allowed_flags,
                                                                    description, num_of_required_values, required_options)

    def add_option(self, option_name: OptionName, description: str, allowed_values: OptionValues = ANY) -> None:
        # TODO: make these separate exceptions
        if not InterfaceValidator.is_option_name_valid(option_name):
            print(f'Unable to add option {option_name} - option name invalid')
        if option_name in self.__interface_options.keys():
            print(f'Unable to add option {option_name} - option with the same name already added')

        # TODO: implement handling of user defined default option value
        self.__interface_options[option_name] = OptionProperties(description, allowed_values, DEFAULT_OPTION_VALUE)

    def add_flag(self, flag_name: FlagName, description: str) -> None:
        # TODO: make these separate exceptions
        if not InterfaceValidator.is_flag_name_valid(flag_name):
            print(f'Unable to add flag {flag_name} - flag name invalid')
        if flag_name in self.__interface_flags.keys():
            print(f'Unable to add flag {flag_name} - flag with the same name already added')

        self.__interface_flags[flag_name] = FlagProperties(description)

    def parse(self) -> ParsedCommand:
        if InterfaceHelper.is_help_required(self.__argv, self.__allow_no_arguments):
            print(f'{InterfaceHelper.get_help(self.__program_name, self.__description, self.__interface_commands, self.__interface_options, self.__interface_flags)}')
            return ParsedCommand('help', [], {}, {})

        command_name: CommandName = ''
        command_values: CommandValues = []
        options: OptionsMap = {}
        flags: FlagsMap = {}

        for i in range(1, len(self.__argv)):
            element: str = self.__argv[i]
            element_type: CommandLineElementType = self.__get_command_line_element_type(element, i)

            if element_type == CommandLineElementType.COMMAND:
                command_name = element
                command_values = self.__parse_command(command_name, i)
            if element_type == CommandLineElementType.OPTION:
                option_name, option_value = self.__parse_option(command_name, element, i)
                options[option_name] = option_value
            if element_type == CommandLineElementType.FLAG:
                flag: FlagName = self.__parse_flag(command_name, element, i)
                flags[flag] = True

        if command_name and command_name in self.__interface_commands.keys():
            for required_option in self.__interface_commands[command_name].required_options:
                if required_option not in options.keys():
                    raise MissingRequiredOption(f'Command {command_name} requires option {required_option}, but such '
                                                f'option has not been provided!')

        for flag_name, flag_properties in self.__interface_flags.items():
            if flag_name not in flags:
                flags[flag_name] = False

        return ParsedCommand(command_name, command_values, options, flags)

    def add_command_handler(self, command_name: CommandName, command_handler: CommandHandlerInterface) -> None:
        if command_name not in self.__interface_commands.keys():
            raise UnsupportedCommand(f'Unable to add command handler! Command {command_name} is not added to command '
                                     f'line interface definition!')

        self.__interface_commands[command_name].command_handler = command_handler

    def run(self) -> None:
        parsed_command: ParsedCommand = self.parse()

        if self.__interface_commands[parsed_command.name].command_handler:
            self.__interface_commands[parsed_command.name].command_handler.run(parsed_command.values,
                                                                               parsed_command.options,
                                                                               parsed_command.flags)
        else:
            raise MissingCommandHandler(f'Unable to run command handler for {parsed_command.name} command! No command '
                                        f'handler has been added for this command.')

    def __get_command_line_element_type(self, element: str, element_position_index: int) -> CommandLineElementType:
        if InterfaceValidator.is_command_name_valid(element) and element_position_index == 1:
            return CommandLineElementType.COMMAND
        if InterfaceValidator.is_option_name_valid(element):
            return CommandLineElementType.OPTION
        if InterfaceValidator.is_flag_name_valid(element):
            return CommandLineElementType.FLAG

        return CommandLineElementType.CUSTOM_VALUE

    def __parse_command(self, command_name: CommandName, command_index: int) -> CommandValues:
        if command_name not in self.__interface_commands.keys():
            similar_commands: str = utils.get_similar_keys(self.__interface_commands, command_name, delimiter='\n')

            raise UnsupportedCommand(f'Command {command_name} is not supported!'
                                     f'{InterfaceHelper.get_hint(similar_commands)}')
        if command_index != 1:
            raise InvalidCommandPosition(f'Detected command {command_name} is not directly after program name!')

        if not self.__interface_commands[command_name].requires_value():
            return []
        elif command_index + self.__interface_commands[command_name].num_of_required_values >= len(self.__argv) or \
             self.__get_command_line_element_type(self.__argv[command_index + 1], command_index + 1) == CommandLineElementType.OPTION or \
             self.__get_command_line_element_type(self.__argv[command_index + 1], command_index + 1) == CommandLineElementType.FLAG:
            raise MissingCommandValue(f'Command {command_name} requires '
                                      f'{self.__interface_commands[command_name].num_of_required_values} value(s), but'
                                      f'they were not provided!')

        values: CommandValues = []

        for i in range(self.__interface_commands[command_name].num_of_required_values):
            command_value: CommandValue = self.__argv[command_index + i + 1]

            if self.__interface_commands[command_name].allowed_values and \
               command_value not in self.__interface_commands[command_name].allowed_values:
                similar_values: str = utils.get_similar_values(self.__interface_commands[command_name].allowed_values,
                                                               command_value,
                                                               delimiter='\n')
                raise UnsupportedCommandValue(f'Unsupported value {command_value} for {command_name} command!'
                                              f'{InterfaceHelper.get_hint(similar_values)}')

            values.append(self.__argv[command_index + i + 1])

        return values

    def __parse_option(self, command_name: CommandName, option_name: OptionName,
                       option_index: int) -> (OptionName, OptionValue):
        if option_name not in self.__interface_options.keys():
            similar_options: str = utils.get_similar_keys(self.__interface_options, option_name, delimiter='\n')

            raise UnsupportedOption(f'Option {option_name} is not supported!{InterfaceHelper.get_hint(similar_options)}')
        if option_index + 1 >= len(self.__argv):
            raise MissingOptionValue(f'Option {option_name} requires value, but no value has been provided!')
        if command_name in self.__interface_commands and \
           option_name not in self.__interface_commands[command_name].allowed_options:
            raise ForbiddenOption(f'Option {option_name} is not allowed for {command_name} command!')

        value: OptionValue = self.__argv[option_index + 1]

        if self.__interface_options[option_name].allowed_values and \
           value not in self.__interface_options[option_name].allowed_values:
            similar_values: str = utils.get_similar_values(self.__interface_options[option_name].allowed_values, value,
                                                           delimiter='\n')
            raise ForbiddenOptionValue(f'Given value {value} for option {option_name} is not allowed!'
                                       f'{InterfaceHelper.get_hint(similar_values)}')

        return option_name, value

    def __parse_flag(self, command_name: CommandName, flag_name: FlagName, flag_index: int) -> FlagName:
        if flag_name not in self.__interface_flags.keys():
            similar_flags: str = utils.get_similar_keys(self.__interface_flags, flag_name, delimiter='\n')

            raise UnsupportedFlag(f'Flag {flag_name} is not supported!{InterfaceHelper.get_hint(similar_flags)}')
        if command_name in self.__interface_commands.keys() and \
           flag_name not in self.__interface_commands[command_name].allowed_flags:
            raise ForbiddenFlag(f'Flag {flag_name} is not allowed for {command_name} command!')

        return self.__argv[flag_index]
